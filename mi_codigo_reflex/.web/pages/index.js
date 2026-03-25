/** @jsxImportSource @emotion/react */


import { Fragment, useCallback, useContext, useEffect, useState } from "react"
import { ColorModeContext, EventLoopContext, StateContexts } from "/utils/context"
import { Event, getBackendURL, isTrue, refs } from "/utils/state"
import { MoonIcon as LucideMoonIcon, SunIcon as LucideSunIcon, TriangleAlertIcon as LucideTriangleAlertIcon, WifiOffIcon as LucideWifiOffIcon } from "lucide-react"
import { keyframes } from "@emotion/react"
import { toast, Toaster } from "sonner"
import env from "/env.json"
import { Box as RadixThemesBox, Button as RadixThemesButton, Callout as RadixThemesCallout, Checkbox as RadixThemesCheckbox, Container as RadixThemesContainer, Flex as RadixThemesFlex, Heading as RadixThemesHeading, Link as RadixThemesLink, Switch as RadixThemesSwitch, Text as RadixThemesText, TextField as RadixThemesTextField } from "@radix-ui/themes"
import Script from "next/script"
import { DebounceInput } from "react-debounce-input"
import NextLink from "next/link"
import NextHead from "next/head"



export function Callout__root_45e2c20799693b82b5e3d3cd650a8b6e () {
  const state__state__login_state = useContext(StateContexts.state__state__login_state)



  return (
    <RadixThemesCallout.Root css={{"display": state__state__login_state.show_email_alert}} size={`1`}>
  <RadixThemesCallout.Text>
  {`Introduce un correo válido`}
</RadixThemesCallout.Text>
</RadixThemesCallout.Root>
  )
}

export function Checkbox_28ee3e7dc1cb9032d434f77eb75c35fc () {
  const state__state__login_state = useContext(StateContexts.state__state__login_state)
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_change_a53cbf35c83f0f5f6951f2ff474182f7 = useCallback((_e0) => addEvents([Event("state.state.login_state.toggleOptionalCheck", {checked:_e0})], (_e0), {}), [addEvents, Event])


  return (
    <RadixThemesCheckbox checked={state__state__login_state.isOptionalChecked} onCheckedChange={on_change_a53cbf35c83f0f5f6951f2ff474182f7} size={`2`}/>
  )
}

export function Container_a199feb875f6e6d277d74c807231d104 () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <RadixThemesContainer css={{"padding": "40px 60px 40px", "width": "90%", "maxWidth": "450px", "position": "absolute", "top": "50%", "left": "50%", "transform": "translate(-50%,-50%)", "background": isTrue(((colorMode) === (`light`))) ? `white` : ["#474747"], "align": "center", "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)"}} size={`3`}>
  <RadixThemesBox>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"maxWidth": "60em"}} direction={`column`} gap={`2`}>
  <RadixThemesHeading css={{"fontSize": "1.5em", "fontFamily": ["Roboto"], "--default-font-family": ["Roboto"], "textAlign": "center"}}>
  {`Test de Personalidad`}
</RadixThemesHeading>
  <RadixThemesText as={`p`} css={{"textAlign": "center", "marginTop": "0.5em"}}>
  {`Introduce tu correo electrónico para acceder al test`}
</RadixThemesText>
  <Debounceinput_19e2d18735d746f476861110c915f731/>
  <Callout__root_45e2c20799693b82b5e3d3cd650a8b6e/>
  <Fragment_4d81898a7c7afdc522d51ac850b33bff/>
  <RadixThemesText as={`label`} size={`1`}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`row`} gap={`3`}>
  <RadixThemesText as={`label`} size={`2`}>
  <RadixThemesFlex gap={`2`}>
  <Checkbox_28ee3e7dc1cb9032d434f77eb75c35fc/>
  {``}
</RadixThemesFlex>
</RadixThemesText>
  {`Acepto las`}
  <Link_891ac29ecc2caf342a78a5efe80f0eaf/>
  {`al test gratuito`}
</RadixThemesFlex>
</RadixThemesText>
  <RadixThemesText as={`label`} size={`1`}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`row`} gap={`3`}>
  <RadixThemesText as={`label`} size={`2`}>
  <RadixThemesFlex gap={`2`}>
  <Checkbox_195fa7d6d668f12754e37ff7750af71c/>
  {``}
</RadixThemesFlex>
</RadixThemesText>
  {`Acepto los`}
  <Link_824188c0002072c584ead86e3a7210fa/>
  {`de la aplicación`}
</RadixThemesFlex>
</RadixThemesText>
  <Callout__root_42aa2a40b96494c825058fb5119de0f0/>
  <Button_5ce69b080b96c1e93b4f2715dfa1d428/>
</RadixThemesFlex>
</RadixThemesBox>
</RadixThemesContainer>
  )
}

export function Debounceinput_19e2d18735d746f476861110c915f731 () {
  const state__state__login_state = useContext(StateContexts.state__state__login_state)
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_change_282d836fed2f735bb835e8282eacf886 = useCallback((_e0) => addEvents([Event("state.state.login_state.update_email", {email:_e0.target.value})], (_e0), {}), [addEvents, Event])


  return (
    <DebounceInput css={{"isPassword": false}} debounceTimeout={300} element={RadixThemesTextField.Root} onChange={on_change_282d836fed2f735bb835e8282eacf886} placeholder={`Correo electrónico`} radius={`none`} size={`3`} type={`email`} value={state__state__login_state.email}/>
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

export function Checkbox_195fa7d6d668f12754e37ff7750af71c () {
  const state__state__login_state = useContext(StateContexts.state__state__login_state)
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_change_bc5fed1f8d400fe28a8c19ed96047839 = useCallback((_e0) => addEvents([Event("state.state.login_state.toggleCheck", {checked:_e0})], (_e0), {}), [addEvents, Event])


  return (
    <RadixThemesCheckbox checked={state__state__login_state.isChecked} onCheckedChange={on_change_bc5fed1f8d400fe28a8c19ed96047839} size={`2`}/>
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


export function Link_891ac29ecc2caf342a78a5efe80f0eaf () {



  return (
    <RadixThemesLink asChild={true} css={{"textDecoration": "none", "&:hover": {"color": "var(--accent-8)"}}} target={isTrue(true) ? `_blank` : ``} weight={`medium`}>
  <NextLink href={`https://academiametodos.com/home/acceso-gratis-al-test-de-personalidad-consentimiento/`} passHref={true}>
  {`condiciones de acceso`}
</NextLink>
</RadixThemesLink>
  )
}

export function Button_5ce69b080b96c1e93b4f2715dfa1d428 () {
  const state__state__login_state = useContext(StateContexts.state__state__login_state)
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_click_67096b833225c60f4c8c9e252bd533e8 = useCallback((_e) => addEvents([Event("state.state.login_state.button_click.click_event", {})], (_e), {}), [addEvents, Event])


  return (
    <RadixThemesButton css={{"padding": "1em", "borderRadius": "0", "backgroundColor": ["#FC4F00"], "&:hover": {"backgroundColor": ["#1B9AAF"]}}} disabled={state__state__login_state.checkStatusButton} loading={state__state__login_state.isWaiting} onClick={on_click_67096b833225c60f4c8c9e252bd533e8} size={`3`}>
  {`Acceder`}
</RadixThemesButton>
  )
}

export function Link_824188c0002072c584ead86e3a7210fa () {



  return (
    <RadixThemesLink asChild={true} css={{"textDecoration": "none", "&:hover": {"color": "var(--accent-8)"}}} target={isTrue(true) ? `_blank` : ``} weight={`medium`}>
  <NextLink href={`https://academiametodos.com/home/terminos-y-condiciones-test-de-personalidad-tropa-y-marineria/`} passHref={true}>
  {`términos y condiciones`}
</NextLink>
</RadixThemesLink>
  )
}

export function Fragment_4d81898a7c7afdc522d51ac850b33bff () {
  const state__state__login_state = useContext(StateContexts.state__state__login_state)



  return (
    <Fragment>
  {isTrue(state__state__login_state.showEmailNotFoundAlert) ? (
  <Fragment>
  <RadixThemesCallout.Root color={`red`} css={{"width": "100%"}} role={`alert`}>
  <RadixThemesCallout.Icon>
  <LucideTriangleAlertIcon css={{"color": "var(--current-color)"}} size={18}/>
</RadixThemesCallout.Icon>
  <RadixThemesCallout.Text css={{"fontSize": "0.8em", "fontStyle": "italic"}}>
  {`No existe una cuenta asociada a este correo`}
</RadixThemesCallout.Text>
</RadixThemesCallout.Root>
</Fragment>
) : (
  <Fragment/>
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

export function Callout__root_42aa2a40b96494c825058fb5119de0f0 () {
  const state__state__login_state = useContext(StateContexts.state__state__login_state)



  return (
    <RadixThemesCallout.Root css={{"display": state__state__login_state.show_terms_alert}} size={`1`}>
  <Fragment/>
  <RadixThemesCallout.Text>
  {`Acepta los términos para poder continuar`}
</RadixThemesCallout.Text>
</RadixThemesCallout.Root>
  )
}

export default function Component() {

  return (
    <Fragment>
  <Fragment>
  <Div_ac2a89ea84667d600a059f034bd91dfe/>
  <Toaster_89416713a273995fc60191a4cf573054/>
</Fragment>
  <RadixThemesBox css={{"height": "100vh", "width": "100%", "background": "linear-gradient(rgba(0,0,0,0.8), rgba(27,154,175,0.8)), url('/tropa.jpg')", "backgroundSize": "cover", "position": "relative", "backgroundPosition": "center"}}>
  <Script strategy={`afterInteractive`}>
  {`
                        document.documentElement.lang='es'`}
</Script>
  <Flex_fe8aa48157a8016f6cd21a6a631d11e2/>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"width": "100%", "height": "100vh"}} direction={`column`} gap={`3`}>
  <Container_a199feb875f6e6d277d74c807231d104/>
</RadixThemesFlex>
</RadixThemesBox>
  <NextHead>
  <title>
  {`Login`}
</title>
  <meta content={`favicon.ico`} property={`og:image`}/>
</NextHead>
</Fragment>
  )
}
