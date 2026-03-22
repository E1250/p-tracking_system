import {eucleadianDistance} from "./equations"


export function isTooClose(newNodePosition, nodes){
    /**
     * Check if the new position is too close to any other node, to avoide overlapping. 
     * @param newNodePosition - Could be the current mouse pos
     * @param nodes - List of nodes to check 
     * @returns bool represents if there is already a node near this pos. 
     */
    for (const node of nodes){   // I just noticed that `of` differ from `in` unline python.  
        const distance = eucleadianDistance(newNodePosition, {x: node.x, y:node.y})
        const MIN_DISTANCE = 0.05
        if (distance < MIN_DISTANCE){
            return true;   // Node is too close to an existing one. 
        }
    }
    return false;  // Node is not close to any other one. 
}

export function alignedLine(oldPoint, newPoint){
    /**
     * Adding a calculated aligned node instead of just random node, it should be 90 aligned.
     * @param oldPoint - the old point module
     * @param newPoint - the new point module
     * @returns point aligned 90deg with it. 
     */
    const dx = Math.abs(oldPoint.x - newPoint.x)
    const dy = Math.abs(oldPoint.y - newPoint.y)
    if ((dx - dy) < 0) {
      return {x: oldPoint.x, y: newPoint.y}
    }
    return {x: newPoint.x, y: oldPoint.y}
  }

import { Node } from "../types/graph";
export function closestPointOnSegment(P:Node, A:Node, B:Node){
    /**
     * @param P - Represents the node around the segment. (Cursor Pos)
     * @param A - Represent the first point that represents the Segment. (Point on the edge)
     * @param B - Represent the second point that represents the Segment.
     * Note that the segment like a line with two ends (Nodes at the end.)
     * @returns point, t (place or percentage on that line.)
     */
    // AB = B - A
    const AB = {x: B.x - A.x, y: B.y - A.y}  // Edge direction vector A -> B
    // AP = P - A
    const AP = {x: P.x - A.x, y: P.y - A.y}  // Vector from A to Cursor (P)

    // AB.x ^ 2 + AB.y ^ 2
    const lengthSq = AB.x * AB.x + AB.y * AB.y

    // A, B are the same point. 
    if (lengthSq === 0) return {point: A, t: 0} 

    // How much AP piont in the direction of AB. 
    const dot = AP.x * AB.x + AP.y * AB.y
    // Normalizing
    const tRaw = dot / lengthSq

    // clamp to [0, 1]
    const t = Math.max(0, Math.min(1, tRaw))

    const point = {
        x: A.x + t * AB.x,
        y: A.y + t * AB.y
    }

    return {point, t}
}

export function findClosestEdgePoint(cursor: Node, nodes: Node[], threshold = 0.05){
    if (nodes.length < 2) return null

    let closest
    let minDist = Infinity

    for (let i = 0; i < nodes.length; i++){
        // Creating the Segment. 
        const A = nodes.at(i - 1)
        const B = nodes[i]

        // Measure how far the cursor is from that closest point
        const {point} = closestPointOnSegment(cursor, A, B)
        const dist = eucleadianDistance(cursor, point)

        if (dist < minDist && dist < threshold){
            minDist = dist
            closest = {point, edgeIndex: i}
        }
    }
    return closest
}