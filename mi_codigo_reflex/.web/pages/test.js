/** @jsxImportSource @emotion/react */


import { Fragment, useCallback, useContext, useEffect, useState } from "react"
import { ColorModeContext, EventLoopContext, StateContexts } from "/utils/context"
import { Event, getBackendURL, isTrue, refs } from "/utils/state"
import { ArrowBigLeftIcon as LucideArrowBigLeftIcon, ArrowBigRightIcon as LucideArrowBigRightIcon, MoonIcon as LucideMoonIcon, SunIcon as LucideSunIcon, WifiOffIcon as LucideWifiOffIcon } from "lucide-react"
import { keyframes } from "@emotion/react"
import { toast, Toaster } from "sonner"
import env from "/env.json"
import { AlertDialog as RadixThemesAlertDialog, Box as RadixThemesBox, Button as RadixThemesButton, Container as RadixThemesContainer, Flex as RadixThemesFlex, Heading as RadixThemesHeading, RadioGroup as RadixThemesRadioGroup, Switch as RadixThemesSwitch, Text as RadixThemesText } from "@radix-ui/themes"
import Script from "next/script"
import { Indicator as RadixProgressIndicator, Root as RadixProgressRoot } from "@radix-ui/react-progress"
import NextHead from "next/head"



export function Heading_8f22e82b2145839fdb2eb3cf909b8403 () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <RadixThemesHeading css={{"fontSize": "2em", "fontFamily": "DIN Next Rounded LT W01 Regular", "--default-font-family": "DIN Next Rounded LT W01 Regular", "color": isTrue(((colorMode) === (`light`))) ? ["#474747"] : `white`}}>
  {`Métodos`}
</RadixThemesHeading>
  )
}

export function Button_180e96b785411362cd5b7883f7d89059 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_click_a55b2e7941e28e7167f55210a8c2f56f = useCallback((_e) => addEvents([Event("_redirect", {path:`/results`,external:false,replace:false})], (_e), {}), [addEvents, Event])


  return (
    <RadixThemesButton css={{"padding": "1em", "borderRadius": "0", "backgroundColor": ["#FC4F00"], "&:hover": {"backgroundColor": ["#1B9AAF"]}}} onClick={on_click_a55b2e7941e28e7167f55210a8c2f56f} variant={`solid`}>
  {`Sí, finalizar`}
</RadixThemesButton>
  )
}

export function Indicator_d6d611ff96cb89d79eeb18024b25301c () {
  const state__test_state = useContext(StateContexts.state__test_state)



  return (
    <RadixProgressIndicator className={`Indicator`} css={{"backgroundColor": ["#FC4F00"], "width": "100%", "height": "100%", "transition": "transform 250ms linear", "&[dataState='loading']": {"transition": "transform 250ms linear"}, "transform": `translateX(calc(-100% + (${state__test_state.current_progress} / 100 * 100%)))`, "boxShadow": "inset 0 0 0 1px var(--gray-a5)"}} max={100} value={state__test_state.current_progress}/>
  )
}

export function Container_c1f9c25a439112e6826d2d7dbd8aac23 () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <RadixThemesContainer css={{"padding": "3.1em 1.8em", "width": "90%", "maxWidth": "37.5em", "margin": "0 auto", "background": isTrue(((colorMode) === (`light`))) ? `white` : ["#474747"], "transform": "translate(-50%, -50%)", "top": "50%", "left": "50%", "position": "absolute", "align": "center", "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)"}} size={`3`}>
  <RadixThemesBox>
  <RadixThemesFlex css={{"display": "flex", "alignItems": "center", "justifyContent": "center", "marginBottom": "1em"}}>
  <RadixThemesHeading>
  {`Progreso Test Personalidad`}
</RadixThemesHeading>
</RadixThemesFlex>
  <RadixProgressRoot className={`Root`} css={{"position": "relative", "overflow": "hidden", "background": "var(--gray-a3)", "borderRadius": "max(var(--radius-2), var(--radius-full))", "width": "100%", "height": "20px", "boxShadow": "inset 0 0 0 1px var(--gray-a5)", "marginBottom": "1em"}} data-radius={`none`}>
  <Indicator_d6d611ff96cb89d79eeb18024b25301c/>
</RadixProgressRoot>
  <RadixThemesBox>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%", "maxWidth": "60em"}} direction={`column`} gap={`2`}>
  <Flex_e4ce9681f2fc76d271a6a3c448146128/>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"marginTop": "1.5em", "width": "100%"}} direction={`row`} gap={`3`}>
  <Fragment>
  <Button_173710e570f3fb72ba770db63efbf5cc/>
</Fragment>
  <RadixThemesFlex css={{"flex": 1, "justifySelf": "stretch", "alignSelf": "stretch"}}/>
  <RadixThemesAlertDialog.Root>
  <RadixThemesAlertDialog.Trigger>
  <RadixThemesButton css={{"padding": "1.5em", "borderRadius": "25px", "backgroundColor": ["#FC4F00"], "&:hover": {"backgroundColor": ["#1B9AAF"]}}}>
  {`Finalizar test`}
</RadixThemesButton>
</RadixThemesAlertDialog.Trigger>
  <Alertdialog__content_b1af89cf5e3c643d7554991d98bfad46/>
</RadixThemesAlertDialog.Root>
  <RadixThemesFlex css={{"flex": 1, "justifySelf": "stretch", "alignSelf": "stretch"}}/>
  <Fragment>
  <Button_afe1347959463f67ca6c7c7d77e11e80/>
</Fragment>
</RadixThemesFlex>
</RadixThemesBox>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"marginTop": "1.5em", "width": "100%"}} direction={`row`} gap={`3`}>
  <Fragment>
  <Button_173710e570f3fb72ba770db63efbf5cc/>
</Fragment>
  <RadixThemesFlex css={{"flex": 1, "justifySelf": "stretch", "alignSelf": "stretch"}}/>
  <Fragment>
  <Button_afe1347959463f67ca6c7c7d77e11e80/>
</Fragment>
</RadixThemesFlex>
  <RadixThemesFlex css={{"display": "flex", "alignItems": "center", "justifyContent": "center", "marginTop": "1em"}}>
  <RadixThemesAlertDialog.Root>
  <RadixThemesAlertDialog.Trigger>
  <RadixThemesButton css={{"padding": "1.5em", "borderRadius": "25px", "backgroundColor": ["#FC4F00"], "&:hover": {"backgroundColor": ["#1B9AAF"]}}}>
  {`Finalizar test`}
</RadixThemesButton>
</RadixThemesAlertDialog.Trigger>
  <Alertdialog__content_b1af89cf5e3c643d7554991d98bfad46/>
</RadixThemesAlertDialog.Root>
</RadixThemesFlex>
</RadixThemesBox>
</RadixThemesFlex>
</RadixThemesBox>
</RadixThemesBox>
</RadixThemesContainer>
  )
}

export function Alertdialog__content_b1af89cf5e3c643d7554991d98bfad46 () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <RadixThemesAlertDialog.Content css={{"maxWidth": 450, "backgroundColor": isTrue(((colorMode) === (`light`))) ? `white` : ["#474747"]}}>
  <RadixThemesAlertDialog.Title>
  {`Finalizar test`}
</RadixThemesAlertDialog.Title>
  <RadixThemesAlertDialog.Description css={{"size": "2"}}>
  {`¿Quieres finalizar el test? Esta acción no es reversible.`}
</RadixThemesAlertDialog.Description>
  <RadixThemesFlex css={{"marginTop": "1em"}} justify={`end`} gap={`3`}>
  <RadixThemesAlertDialog.Cancel>
  <RadixThemesButton css={{"padding": "1em", "borderRadius": "0", "backgroundColor": ["#E8E8E8"], "&:hover": {"backgroundColor": ["#1B9AAF"]}}} variant={`soft`}>
  {`No, seguir el test`}
</RadixThemesButton>
</RadixThemesAlertDialog.Cancel>
  <RadixThemesAlertDialog.Action>
  <RadixThemesFlex>
  <Button_180e96b785411362cd5b7883f7d89059/>
</RadixThemesFlex>
</RadixThemesAlertDialog.Action>
</RadixThemesFlex>
</RadixThemesAlertDialog.Content>
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

export function Flex_e4ce9681f2fc76d271a6a3c448146128 () {
  const state__test_state = useContext(StateContexts.state__test_state)
  const [addEvents, connectErrors] = useContext(EventLoopContext);



  return (
    <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"width": "100%"}} direction={`column`} gap={`3`}>
  {state__test_state.current_data.map((item, index) => (
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"marginTop": "1em"}} direction={`column`} key={index} gap={`3`}>
  <RadixThemesHeading>
  {`${((((state__test_state.pag_actual) * (state__test_state.num_preguntas)) + (index)) + (1))}. ${item["PREGUNTA"]}`}
</RadixThemesHeading>
  <RadixThemesRadioGroup.Root color={`orange`} defaultValue={``} key={(((state__test_state.pag_actual) * (state__test_state.num_preguntas)) + (index))} onValueChange={(_e0) => addEvents([Event("state.test_state.set_selection", {index:(((state__test_state.pag_actual) * (state__test_state.num_preguntas)) + (index)),value:_e0})], (_e0), {})} size={`2`} value={state__test_state.selections[(((state__test_state.pag_actual) * (state__test_state.num_preguntas)) + (index))]}>
  <RadixThemesFlex direction={`column`} gap={`2`}>
  {["Si", "Muchas veces", "Alguna vez", "Pocas veces", "No"].map((value, index_3cc580f763bde3ad) => (
  <RadixThemesText as={`label`} key={index_3cc580f763bde3ad} size={`2`}>
  <RadixThemesFlex gap={`2`}>
  <RadixThemesRadioGroup.Item value={isTrue(((typeof value) === (`string`))) ? value : JSON.stringify(value)}/>
  {isTrue(((typeof value) === (`string`))) ? value : JSON.stringify(value)}
</RadixThemesFlex>
</RadixThemesText>
))}
</RadixThemesFlex>
</RadixThemesRadioGroup.Root>
</RadixThemesFlex>
))}
</RadixThemesFlex>
  )
}

export function Button_afe1347959463f67ca6c7c7d77e11e80 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_click_38707b726267932405ec5224fe7bc785 = useCallback((_e) => addEvents([Event("state.test_state.next_page", {})], (_e), {}), [addEvents, Event])


  return (
    <RadixThemesButton css={{"padding": "1.5em", "borderRadius": "25px", "backgroundColor": ["#FC4F00"], "&:hover": {"backgroundColor": ["#1B9AAF"]}}} onClick={on_click_38707b726267932405ec5224fe7bc785}>
  {`Siguiente`}
  <LucideArrowBigRightIcon css={{"color": "var(--current-color)"}}/>
</RadixThemesButton>
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

export function Button_173710e570f3fb72ba770db63efbf5cc () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_click_765e239ec11379422588a62df1838401 = useCallback((_e) => addEvents([Event("state.test_state.previous_page", {})], (_e), {}), [addEvents, Event])


  return (
    <RadixThemesButton css={{"padding": "1.5em", "borderRadius": "25px", "backgroundColor": ["#FC4F00"], "&:hover": {"backgroundColor": ["#1B9AAF"]}}} onClick={on_click_765e239ec11379422588a62df1838401}>
  <LucideArrowBigLeftIcon css={{"color": "var(--current-color)"}}/>
  {`Anterior`}
</RadixThemesButton>
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

export function Switch_e718961ce6ef9fa7745102ae015f5a3e () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_change_9922dd3e837b9e087c86a2522c2c93f8 = useCallback(toggleColorMode, [addEvents, Event, colorMode, toggleColorMode])


  return (
    <RadixThemesSwitch checked={((colorMode) !== ("light"))} onCheckedChange={on_change_9922dd3e837b9e087c86a2522c2c93f8}/>
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
  <Container_c1f9c25a439112e6826d2d7dbd8aac23/>
</RadixThemesFlex>
</RadixThemesBox>
  <NextHead>
  <title>
  {`Test`}
</title>
  <meta content={`favicon.ico`} property={`og:image`}/>
</NextHead>
</Fragment>
  )
}
