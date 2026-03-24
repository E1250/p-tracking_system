import useImage from "use-image"
import {Image as KonvaImage} from "react-konva"
import React, { useEffect, useState } from 'react'

export function FloorBackground({bgURL, width, height}){
  
  const [image, setImage] = useState<HTMLImageElement | null>(null)
  
  useEffect(() => {
    if (!bgURL) return

    const img = new window.Image()
    img.src = bgURL
    img.onload = () => setImage(img)
  }, [bgURL])

  if (!image) return null

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