export interface Node{
  id?:string
  x:number
  y:number
  angle?:number
  subPoints?:number[]
}

export interface Room{
  id:string
  nodes:Node[]
  cameras:Node[]
}

export interface Floor{
  floorName: string
  rooms: Room[]
  bgURL: string
}

export type EditorMode = "edit" | "camera" | "view" | "draw"