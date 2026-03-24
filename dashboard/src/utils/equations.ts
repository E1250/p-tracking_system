// the {} in function, means i can direclty use the prop, as they are directly values.  
export function lerp(startPoint:number, endPoint:number, t:number): number{
    return startPoint + t * (endPoint - startPoint)
}

import {Node} from '../types/graph'
export function eucleadianDistance(point1:Node, point2:Node): number{
  const dx = point1.x - point2.x
  const dy = point1.y - point2.y
  return Math.sqrt(dx * dx + dy * dy) // X^2 + Y^2
}

export function angleTo(fromPoint: Node, toPoint: Node):number{
  /**
   * It converts a direction vector into an angle in degree
   * @param fromPoint 
   * @param toPoint
   * @returns degree
   */
  return Math.atan2(toPoint.y - fromPoint.y, toPoint.x - fromPoint.x) * (180 / Math.PI)
}

