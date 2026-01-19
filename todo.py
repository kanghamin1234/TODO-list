import json
import os
from datetime import datetime

class TodoApp:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """파일에서 할 일 목록을 불러옵니다."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def save_tasks(self):
        """할 일 목록을 파일에 저장합니다."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, indent=4, ensure_ascii=False)

    def add_task(self, title, due_date=""):
        """새로운 할 일을 추가합니다."""
        self.tasks.append({"title": title, "completed": False, "due_date": due_date})
        self.save_tasks()
        print(f"✅ 할 일 '{title}'이(가) 추가되었습니다.")

    def list_tasks(self):
        """할 일 목록을 출력합니다."""
        if not self.tasks:
            print("\n📭 할 일 목록이 비어있습니다.")
            return

        print("\n📝 --- 할 일 목록 ---")
        today = datetime.now().strftime("%Y-%m-%d")

        for idx, task in enumerate(self.tasks, 1):
            status = "[x]" if task['completed'] else "[ ]"
            due_date = task.get('due_date', "")
            due_str = f" (마감: {due_date})" if due_date else ""
            line = f"{idx}. {status} {task['title']}{due_str}"

            if due_date and not task['completed'] and due_date < today:
                print(f"\033[91m{line} (⚠️ 기한 지남)\033[0m")
            else:
                print(line)
        print("---------------------\n")

    def complete_task(self, index):
        """특정 할 일을 완료 상태로 변경합니다."""
        if 1 <= index <= len(self.tasks):
            self.tasks[index-1]['completed'] = True
            self.save_tasks()
            print("🎉 완료 처리되었습니다!")
        else:
            print("❌ 잘못된 번호입니다.")

    def delete_task(self, index):
        """특정 할 일을 삭제합니다."""
        if 1 <= index <= len(self.tasks):
            removed = self.tasks.pop(index-1)
            self.save_tasks()
            print(f"🗑️ '{removed['title']}' 삭제되었습니다.")
        else:
            print("❌ 잘못된 번호입니다.")

def main():
    app = TodoApp()
    
    while True:
        print("\n1. 할 일 추가 | 2. 목록 보기 | 3. 완료 처리 | 4. 삭제 | 5. 종료")
        choice = input("선택하세요: ")

        if choice == '1':
            title = input("할 일 내용을 입력하세요: ")
            due_date = input("마감 기한을 입력하세요 (예: 2023-12-31, 엔터로 건너뛰기): ")
            app.add_task(title, due_date)
        elif choice == '2':
            app.list_tasks()
        elif choice == '3':
            app.list_tasks()
            idx = int(input("완료할 할 일 번호를 입력하세요: "))
            app.complete_task(idx)
        elif choice == '4':
            app.list_tasks()
            idx = int(input("삭제할 할 일 번호를 입력하세요: "))
            app.delete_task(idx)
        elif choice == '5':
            print("👋 프로그램을 종료합니다.")
            break
        else:
            print("올바른 번호를 선택해주세요.")

if __name__ == "__main__":
    main()