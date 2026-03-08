(globalThis.TURBOPACK||(globalThis.TURBOPACK=[])).push(["object"==typeof document?document.currentScript:void 0,79843,e=>{"use strict";var r=e.i(87433),a=e.i(47163);function i({className:e,reverse:i=!1,pauseOnHover:l=!1,vertical:t=!1,repeat:n=4,duration:m="40s",gap:s="1rem",children:o,...c}){let u=Array(n).fill(0).map((e,a)=>(0,r.jsx)("div",{className:"flex shrink-0",style:{gap:s},children:o},a));return(0,r.jsxs)(r.Fragment,{children:[(0,r.jsx)("style",{children:`
        @keyframes marquee {
          from { transform: translateX(0); }
          to { transform: translateX(calc(-100% - ${s})); }
        }
        @keyframes marquee-vertical {
          from { transform: translateY(0); }
          to { transform: translateY(calc(-100% - ${s})); }
        }

        .marquee {
          display: flex;
          animation: marquee ${m} linear infinite;
          animation-direction: ${i?"reverse":"normal"};
        }

        .marquee-vertical {
          display: flex;
          flex-direction: column;
          animation: marquee-vertical ${m} linear infinite;
          animation-direction: ${i?"reverse":"normal"};
        }

        .marquee-hover:hover,
        .marquee-vertical-hover:hover {
          animation-play-state: paused;
        }
      `}),(0,r.jsx)("div",{...c,className:(0,a.cn)("overflow-hidden flex",t?"flex-col":"flex-row",e),children:(0,r.jsx)("div",{className:(0,a.cn)(t?l?"marquee-vertical-hover marquee-vertical":"marquee-vertical":l?"marquee-hover marquee":"marquee"),children:u})})]})}e.s(["Marquee",()=>i])}]);