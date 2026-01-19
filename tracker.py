import sys, json, os, datetime

def search_task(id):
    tasks = load_tasks()
    start,end=0,len(tasks)-1
    while start<=end:
        mid=(start+end)//2
        if tasks[mid]['id']==id:
            return mid
        elif tasks[mid]['id']<id:
            start=mid+1
        else:
            end=mid-1
    return None

def load_tasks():
    if not os.path.exists("tasks.json"):
        return []
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, ValueError):
        return []

def save_tasks(tasks):
    tasks.sort(key=lambda x:x['id'])
    with open("tasks.json", "w") as file:
        json.dump(tasks, file,indent=4)


def add_task():
    tasks = load_tasks()
    nuevo={
        'id':tasks[-1]['id']+1 if tasks else 1,
        'description':sys.argv[2],
        'status':'todo',
        'created_at':datetime.datetime.now().isoformat(),
        'updated_at':datetime.datetime.now().isoformat(),
    }
    tasks.append(nuevo)
    save_tasks(tasks)

def delete_task():
    task=search_task(int(sys.argv[2]))
    tasks = load_tasks()
    if task:
        tasks.pop(task)
        save_tasks(tasks)

def update_task():
    task=search_task(int(sys.argv[2]))
    tasks = load_tasks()
    if task:
        if sys.argv[1] == "update":
            tasks[task]['description']=sys.argv[3]
        elif sys.argv[1] == "mark-in-progress":
            tasks[task]['status']='in-progress'
        elif sys.argv[1] == "mark-done":
            tasks[task]['status']='done'
        tasks[task]['updated_at']=datetime.datetime.now().isoformat()
        save_tasks(tasks)

def list_tasks():
    if len(sys.argv) > 2 and sys.argv[2] in ['done','in-progress','todo']:
        tasks=load_tasks()
        for task in tasks:
            if task['status']==sys.argv[2]:
                print(f"{task['id']}. {task['description']} - {task['status']}")
    else:
        tasks=load_tasks()
        for task in tasks:
            print(f"{task['id']}. {task['description']} - {task['status']}")

def main():
    if len(sys.argv) < 2:
        sys.exit("Modo de uso: python tracker.py <tasks>")
    
    if sys.argv[1] == "add":
        add_task()

    elif sys.argv[1] == "delete":
        delete_task()

    elif sys.argv[1] in ["update","mark-in-progress","mark-done"]:
        update_task()


    elif sys.argv[1] == "list":
        list_tasks()

    else:
        sys.exit("Modo de uso: python tracker.py <tasks>")    

if __name__ == "__main__":
    main()