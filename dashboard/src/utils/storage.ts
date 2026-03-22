const STORAGE_KEY = "dashboard_floors"

export function saveFloorsState(state){
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
    console.log("Saved Item Successfully...")
}

export function loadFloorsState<T>(fallback){
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return fallback
    return JSON.parse(raw) as T
}

export function clearFloorState(){
    localStorage.removeItem(STORAGE_KEY)
}

export function exportFloors(state){
    // Convert to JSON
    const json = JSON.stringify(state, null, 2) // 2 -> Print with 2 space indent
    // Binary Large Object
    const blob = new Blob([json], {type: "application/json"});
    // Create a temp url
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a")
    a.href = url
    a.download = "floors.json"
    a.click()
    
    // Release the temp url from memory
    URL.revokeObjectURL(url)
}

export function importFloors(e, isSuccess: (data)=> void){
    const file = e.target.files?.[0]
    if (!file) return;

    const reader = new FileReader()
    reader.onload = (e) => {
        const parsed = JSON.parse(e.target?.result as string) as Floor[];
        isSuccess(parsed)
    }
    reader.readAsText(file)
}