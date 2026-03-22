import React from "react"

// Note that interface working in two cases, specify the types of inputs (like Pydantic) or specfy the return of your function. 
export function IconButton({label, onClick, icon, style={}}){
  //Note that it must start with a capitcal letter, or it will cause an error. 
    return (
      <button onClick={onClick} title={label} style={{
        backgroundColor:"transparent",
        display:"flex",
        flexDirection: "column",
        justifyContent:"center",
        alignItems:"center",
        ...style
      }}>
          <img src={icon} className='mode-button' width={50} height={50} alt={label}/>
          <span>{label}</span>
        </button>
    )
}