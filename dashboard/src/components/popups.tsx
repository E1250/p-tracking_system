import React from "react"

export function ShortcutsPopup({close}: {close: () => void}){
    return (
        <div onClick={() => {close()}} style={{
            position:"fixed",
            background:"rgba(0,0,0,0.6)",
            justifyContent:"center",
            alignItems:"center",
            display:"flex",
            flexDirection:"column",
            inset: 0
        }}>
            <h3 style={{marginBottom: 16}}>Keyboard Shortcuts</h3>
            <table style={{borderSpacing: "12px 8px", width:"200", height:"200"}}>
                <tbody>
                    <tr>
                        <td><kbd>Delete</kbd></td>
                        <td>Delete Full dashboard data</td>
                    </tr>
                    <tr>
                        <td><kbd>Esc</kbd></td>
                        <td>Move to View Mode</td>
                    </tr>
                </tbody>
            </table>
        </div>
    )
}