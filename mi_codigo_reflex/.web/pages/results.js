/** @jsxImportSource @emotion/react */


import { Fragment, useCallback, useContext, useEffect, useState } from "react"
import { ColorModeContext, EventLoopContext, StateContexts } from "/utils/context"
import { Event, getBackendURL, isTrue, refs } from "/utils/state"
import { CircleCheckBigIcon as LucideCircleCheckBigIcon, CircleXIcon as LucideCircleXIcon, MoonIcon as LucideMoonIcon, SunIcon as LucideSunIcon, WifiOffIcon as LucideWifiOffIcon } from "lucide-react"
import { keyframes } from "@emotion/react"
import { toast, Toaster } from "sonner"
import env from "/env.json"
import { Box as RadixThemesBox, Button as RadixThemesButton, Container as RadixThemesContainer, Flex as RadixThemesFlex, Heading as RadixThemesHeading, Switch as RadixThemesSwitch, Text as RadixThemesText } from "@radix-ui/themes"
import Script from "next/script"
import { Indicator as RadixProgressIndicator, Root as RadixProgressRoot } from "@radix-ui/react-progress"
import NextHead from "next/head"



export function Fragment_cdb6b747ec91b28fd45feff4767034cf () {
  const state__results_state = useContext(StateContexts.state__results_state)



  return (
    <Fragment>
  {isTrue(state__results_state.is_5_ok) ? (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#1B9AAF"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_5) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_5) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
) : (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#FC4F00"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_5) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_5) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
)}
</Fragment>
  )
}

export function Fragment_445b87177c796b47d763094f75f3e0b5 () {
  const state__results_state = useContext(StateContexts.state__results_state)



  return (
    <Fragment>
  {isTrue(state__results_state.is_3_ok) ? (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#1B9AAF"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_3) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_3) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
) : (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#FC4F00"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_3) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_3) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
)}
</Fragment>
  )
}

export function Toaster_89416713a273995fc60191a4cf573054 () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)


  refs['__toast'] = toast
  const [addEvents, connectErrors] = useContext(EventLoopContext);
  
const toast_props = {"description": `Check if server is reachable at ${getBackendURL(env.EVENT).href}`, "closeButton": true, "duration": 120000, "id": "websocket-error"};
const [userDismissed, setUserDismissed] = useState(false);
useEffect(() => {
    if (connectErrors.length >= 2) {
        if (!userDismissed) {
            toast.error(
                `Cannot connect to server: ${(connectErrors.length > 0) ? connectErrors[connectErrors.length - 1].message : ''}.`,
                {...toast_props, onDismiss: () => setUserDismissed(true)},
            )
        }
    } else {
        toast.dismiss("websocket-error");
        setUserDismissed(false);  // after reconnection reset dismissed state
    }
}, [connectErrors]);

  return (
    <Toaster closeButton={false} expand={true} position={`bottom-right`} richColors={true} theme={colorMode}/>
  )
}

export function Fragment_2575017f651ce7bb27e3debd9afeb9fc () {
  const state__results_state = useContext(StateContexts.state__results_state)



  return (
    <Fragment>
  {isTrue(state__results_state.isUserApto) ? (
  <Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`row`} gap={`3`}>
  <LucideCircleCheckBigIcon css={{"color": ["#1B9AAF"], "strokeWidth": 3, "marginTop": "0.2em"}}/>
  <RadixThemesHeading css={{"color": ["#1B9AAF"]}}>
  {`Apto`}
</RadixThemesHeading>
</RadixThemesFlex>
</Fragment>
) : (
  <Fragment>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`row`} gap={`3`}>
  <LucideCircleXIcon css={{"color": ["#FC4F00"], "strokeWidth": 3, "marginTop": "0.2em"}}/>
  <RadixThemesHeading css={{"color": ["#FC4F00"]}}>
  {`No apto`}
</RadixThemesHeading>
</RadixThemesFlex>
</Fragment>
)}
</Fragment>
  )
}

export function Fragment_99ff3f03f2a27684fc6a3e50d6d8ff2f () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <Fragment>
  {isTrue(((colorMode) === (`light`))) ? (
  <Fragment>
  <LucideSunIcon css={{"color": "var(--current-color)"}}/>
</Fragment>
) : (
  <Fragment>
  <LucideMoonIcon css={{"color": "var(--current-color)"}}/>
</Fragment>
)}
</Fragment>
  )
}

export function Fragment_39430aaf16f3cd117a5ee5be7218c95b () {
  const state__results_state = useContext(StateContexts.state__results_state)



  return (
    <Fragment>
  {isTrue(state__results_state.is_4_ok) ? (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#1B9AAF"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_4) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_4) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
) : (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#FC4F00"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_4) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_4) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
)}
</Fragment>
  )
}

export function Container_0a08c74b11151b38a02296a775bdf2fc () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <RadixThemesContainer css={{"padding": "40px 60px 40px", "width": "90%", "maxWidth": "450px", "marginTop": "4.5em", "marginBottom": "50%", "background": isTrue(((colorMode) === (`light`))) ? `white` : ["#474747"], "align": "center", "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)"}} size={`3`}>
  <RadixThemesBox>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"maxWidth": "60em"}} direction={`column`} gap={`2`}>
  <Fragment_2575017f651ce7bb27e3debd9afeb9fc/>
  <RadixThemesHeading>
  {`Resultados del test`}
</RadixThemesHeading>
  <RadixThemesText as={`p`}>
  {`Sinceridad`}
</RadixThemesText>
  <Fragment_ee87dd2a8faef7842647f48889d70a0e/>
  <RadixThemesText as={`p`}>
  {`Extraversión`}
</RadixThemesText>
  <Fragment_5aebf6553ddabc5dd1e19b18058b1b53/>
  <RadixThemesText as={`p`}>
  {`Depresión`}
</RadixThemesText>
  <Fragment_445b87177c796b47d763094f75f3e0b5/>
  <RadixThemesText as={`p`}>
  {`Neuroticismo`}
</RadixThemesText>
  <Fragment_39430aaf16f3cd117a5ee5be7218c95b/>
  <RadixThemesText as={`p`}>
  {`Psicoticismo`}
</RadixThemesText>
  <Fragment_cdb6b747ec91b28fd45feff4767034cf/>
  <RadixThemesText as={`p`}>
  {`Paranoidismo`}
</RadixThemesText>
  <Fragment_c209652c0022207211cee0daae62b79a/>
  <RadixThemesText as={`p`}>
  {`Desviación Psicopática`}
</RadixThemesText>
  <Fragment_fee7bdfdd9af027b7bb3f825036d73fc/>
  <Button_6792b579e034d506e00fb8888c83f33f/>
</RadixThemesFlex>
</RadixThemesBox>
</RadixThemesContainer>
  )
}

export function Div_ac2a89ea84667d600a059f034bd91dfe () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    <div css={{"position": "fixed", "width": "100vw", "height": "0"}} title={`Connection Error: ${(connectErrors.length > 0) ? connectErrors[connectErrors.length - 1].message : ''}`}>
  <Fragment_cf53a535ae2e610a113dd361eb6ac95b/>
</div>
  )
}

export function Fragment_cf53a535ae2e610a113dd361eb6ac95b () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    <Fragment>
  {isTrue(connectErrors.length > 0) ? (
  <Fragment>
  <LucideWifiOffIcon css={{"color": "crimson", "zIndex": 9999, "position": "fixed", "bottom": "33px", "right": "33px", "animation": `${pulse} 1s infinite`}} size={32}/>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  )
}

const pulse = keyframes`
    0% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
`


export function Button_6792b579e034d506e00fb8888c83f33f () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_click_a708b94666a03f36a060bd3d850534f9 = useCallback((_e) => addEvents([Event("state.state.logout", {})], (_e), {}), [addEvents, Event])


  return (
    <RadixThemesButton css={{"padding": "1em", "borderRadius": "0", "backgroundColor": ["#FC4F00"], "&:hover": {"backgroundColor": ["#1B9AAF"]}}} onClick={on_click_a708b94666a03f36a060bd3d850534f9}>
  {`Salir`}
</RadixThemesButton>
  )
}

export function Fragment_c209652c0022207211cee0daae62b79a () {
  const state__results_state = useContext(StateContexts.state__results_state)



  return (
    <Fragment>
  {isTrue(state__results_state.is_6_ok) ? (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#1B9AAF"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_6) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_6) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
) : (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#FC4F00"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_6) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_6) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
)}
</Fragment>
  )
}

export function Fragment_fee7bdfdd9af027b7bb3f825036d73fc () {
  const state__results_state = useContext(StateContexts.state__results_state)



  return (
    <Fragment>
  {isTrue(state__results_state.is_7_ok) ? (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#1B9AAF"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_7) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_7) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
) : (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#FC4F00"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_7) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_7) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
)}
</Fragment>
  )
}

export function Fragment_5aebf6553ddabc5dd1e19b18058b1b53 () {
  const state__results_state = useContext(StateContexts.state__results_state)



  return (
    <Fragment>
  {isTrue(state__results_state.is_2_ok) ? (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#1B9AAF"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_2) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_2) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
) : (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#FC4F00"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_2) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_2) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
)}
</Fragment>
  )
}

export function Flex_fe8aa48157a8016f6cd21a6a631d11e2 () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"position": "fixed", "top": "0px", "backgroundColor": isTrue(((colorMode) === (`light`))) ? `white` : ["#474747"], "padding": "1em", "height": "4em", "width": "100%", "zIndex": "5"}} direction={`row`} gap={`3`}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`row`} gap={`3`}>
  <img css={{"width": "2em"}} src={`/metodos_naranja_thick.svg`}/>
  <Heading_8f22e82b2145839fdb2eb3cf909b8403/>
</RadixThemesFlex>
  <RadixThemesFlex css={{"flex": 1, "justifySelf": "stretch", "alignSelf": "stretch"}}/>
  <Fragment_99ff3f03f2a27684fc6a3e50d6d8ff2f/>
  <Switch_e718961ce6ef9fa7745102ae015f5a3e/>
</RadixThemesFlex>
  )
}

export function Heading_8f22e82b2145839fdb2eb3cf909b8403 () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <RadixThemesHeading css={{"fontSize": "2em", "fontFamily": "DIN Next Rounded LT W01 Regular", "--default-font-family": "DIN Next Rounded LT W01 Regular", "color": isTrue(((colorMode) === (`light`))) ? ["#474747"] : `white`}}>
  {`Métodos`}
</RadixThemesHeading>
  )
}

export function Switch_e718961ce6ef9fa7745102ae015f5a3e () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_change_9922dd3e837b9e087c86a2522c2c93f8 = useCallback(toggleColorMode, [addEvents, Event, colorMode, toggleColorMode])


  return (
    <RadixThemesSwitch checked={((colorMode) !== ("light"))} onCheckedChange={on_change_9922dd3e837b9e087c86a2522c2c93f8}/>
  )
}

export function Fragment_ee87dd2a8faef7842647f48889d70a0e () {
  const state__results_state = useContext(StateContexts.state__results_state)



  return (
    <Fragment>
  {isTrue(state__results_state.is_1_ok) ? (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#1B9AAF"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_1) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_1) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
) : (
  <Fragment>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "0em"}} data-radius={`none`}>
  <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#FC4F00"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${(((state__results_state.score_item_1) / (95)) * (100))} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={(((state__results_state.score_item_1) / (95)) * (100))}/>
</RadixProgressRoot>
</Fragment>
)}
</Fragment>
  )
}

export default function Component() {

  return (
    <Fragment>
  <Fragment>
  <Div_ac2a89ea84667d600a059f034bd91dfe/>
  <Toaster_89416713a273995fc60191a4cf573054/>
</Fragment>
  <RadixThemesBox css={{"height": "100vh", "width": "100%", "background": "linear-gradient(rgba(0,0,0,0.8), rgba(27,154,175,0.8)), url('/tropa.jpg')", "backgroundSize": "cover", "backgroundAttachment": "fixed", "position": "relative", "backgroundPosition": "center", "backgroundRepeat": "no-repeat"}}>
  <Script strategy={`afterInteractive`}>
  {`
                        document.documentElement.lang='es'
                        document.addEventListener('contextmenu', event => event.preventDefault());`}
</Script>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%", "height": "100vh"}} direction={`column`} gap={`3`}>
  <Flex_fe8aa48157a8016f6cd21a6a631d11e2/>
  <Container_0a08c74b11151b38a02296a775bdf2fc/>
</RadixThemesFlex>
</RadixThemesBox>
  <NextHead>
  <title>
  {`Resultados`}
</title>
  <meta content={`favicon.ico`} property={`og:image`}/>
</NextHead>
</Fragment>
  )
}
