Starting with the front end sounds great and challenging. After some search I decided to use React.JS 
You can start using react by downloading Node.js, it is like the engine. 

### Installing node js. 
Feel free to use this link - https://nodejs.org/en/download 
Then check if it was insalled using these commands. 
```cmd
node -v
npm -v
```

Also for the maps, i see this one is really great, still aim to test it. 
* https://leafletjs.com/
```cmd
npm install leaflet
```

### Create the project
Move to the project dir, and use this (Use the powershell)  Note that i am using `-ts`, it is better and more advanced.
```cmd
npm create vite@latest my-floorplan-app -- --template react-ts
```

And to run the server
```
npm run dev
```

Build the app before deployment. 
```
npm run build
```

I also asked a question, where these new packages are being installed, the answer were in the project itself. 

I also thought of some animation, react has some great bunch of animations, but i aimed to use this also, it make things easier.
```cmd
npm install motion
```

And i used this resource to learn react. 
* https://react.dev/learn

For the canvas part in vanilla code, it has a better way in react, called Kanva
```cmd
npm install react-konva konva
```

The first thing i faced, it was really bad issue for me, some code actually wasn't work, i did't know why at first, after searching it was `jsx` the files was on, but the recommended one was `tsx`. Also Grok didn't recommend `jsx` that came with the project, and advised continuing with `tsx`.
it took some time for me to realize. but i am good now, heeh. move to `tsx` mate.

`tsx` that contains JSX like `div` and so on. `.ts` pure TypeScript. 

After tons of pain in the nech due to trying to modify things in the immutable lists, or as mentioned before, Deeply nested immutable updates. i just found a helper, `immer` js package to help further with this. 
Note that immer is also sensitive to returns, make sure you use always `{}` after `=>`. Curly braces {} every time with Immer. No exceptions.

This is the dashboard link on vercel - https://p-tracking-system-y2dv.vercel.app/


It was suggested that i use version control like this,
Common types:

feat — new feature
fix — bug fix
refactor — restructuring, no behavior change
chore — config, tooling, CI
docs — documentation only 

mention the type: more details about it. 