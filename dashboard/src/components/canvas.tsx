import useImage from "use-image"
import {Image as KonvaImage} from "react-konva"
import React from 'react'

export function Background({url, width, height}){
  const [image] = useImage(url)
  return (
    <KonvaImage 
      image={image}
      width={width}
      height={height}
      x={0}
      y={0}
    />
  )
}