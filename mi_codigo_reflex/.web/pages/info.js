/** @jsxImportSource @emotion/react */


import { Fragment, useCallback, useContext, useEffect, useState } from "react"
import { ColorModeContext, EventLoopContext } from "/utils/context"
import { Event, getBackendURL, isTrue, refs } from "/utils/state"
import { MoonIcon as LucideMoonIcon, SunIcon as LucideSunIcon, WifiOffIcon as LucideWifiOffIcon } from "lucide-react"
import { keyframes } from "@emotion/react"
import { toast, Toaster } from "sonner"
import env from "/env.json"
import { Box as RadixThemesBox, Button as RadixThemesButton, Flex as RadixThemesFlex, Heading as RadixThemesHeading, Link as RadixThemesLink, Switch as RadixThemesSwitch, Tabs as RadixThemesTabs, Text as RadixThemesText } from "@radix-ui/themes"
import Script from "next/script"
import NextLink from "next/link"
import NextHead from "next/head"



export function Box_097dbefe2c9a0bd90e3eb20751a3be93 () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <RadixThemesBox css={{"backgroundColor": isTrue(((colorMode) === (`light`))) ? `#FBE6CC` : ["#B2B2B2"], "borderRadius": "3px", "padding": "8px", "width": "100%", "textAlign": "center"}}>
  {`SI`}
</RadixThemesBox>
  )
}

export function Box_0f698ff7a7a3cb7838146be9a5c5e574 () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <RadixThemesBox css={{"background": isTrue(((colorMode) === (`light`))) ? `white` : ["#474747"]}}>
  <Script strategy={`afterInteractive`}>
  {`
                        document.documentElement.lang='es'`}
</Script>
  <Flex_fe8aa48157a8016f6cd21a6a631d11e2/>
  <RadixThemesFlex css={{"display": "flex", "alignItems": "center", "justifyContent": "center", "paddingTop": "4em"}}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"flex": "1", "maxWidth": "600px", "width": "100%", "marginTop": "2em", "marginBottom": "2em"}} direction={`column`} gap={`3`}>
  <RadixThemesBox css={{"margin": "1em"}}>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} direction={`column`} gap={`3`}>
  <img align={`center`} css={{"width": "100px", "height": "auto", "display": "flex", "direction": "column"}} src={`/ic_test_personalidad.png`}/>
  <RadixThemesHeading css={{"color": ["#1B9AAF"], "fontFamily": ["Roboto"], "--default-font-family": ["Roboto"]}}>
  {`TEST DE PERSONALIDAD`}
</RadixThemesHeading>
  <RadixThemesText as={`p`}>
  {`La prueba de Personalidad forma parte de la segunda fase de la oposición de Tropa y Marinería. 
También se hace por ordenador. En él debes responder a cada una de las preguntas eligiendo una de las cinco 
opciones que tendrás y que siempre son las mismas:`}
</RadixThemesText>
  <RadixThemesFlex css={{"flex": 1, "justifySelf": "stretch", "alignSelf": "stretch"}}/>
  <RadixThemesBox css={{"width": "100%", "@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"textAlign": "center"}} direction={`row`} gap={`3`}>
  <Box_097dbefe2c9a0bd90e3eb20751a3be93/>
  <Box_045dd26aef07260269fa66f5fc35475c/>
  <Box_d7908424bebc27ea2f94eab62d6a3dd6/>
  <Box_1d145a476a1e8d09efc39ace50d76e4a/>
  <Box_e4f74c0124d5bac2bd1a273bceec6a1e/>
</RadixThemesFlex>
</RadixThemesBox>
  <RadixThemesBox css={{"width": "100%", "@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} css={{"textAlign": "center"}} direction={`column`} gap={`3`}>
  <Box_097dbefe2c9a0bd90e3eb20751a3be93/>
  <Box_045dd26aef07260269fa66f5fc35475c/>
  <Box_d7908424bebc27ea2f94eab62d6a3dd6/>
  <Box_1d145a476a1e8d09efc39ace50d76e4a/>
  <Box_e4f74c0124d5bac2bd1a273bceec6a1e/>
</RadixThemesFlex>
</RadixThemesBox>
  <RadixThemesFlex css={{"flex": 1, "justifySelf": "stretch", "alignSelf": "stretch"}}/>
  <RadixThemesHeading css={{"color": ["#1B9AAF"], "fontFamily": ["Roboto"], "--default-font-family": ["Roboto"]}} size={`5`}>
  {`¿Qué evalúan en el Test de Personalidad?`}
</RadixThemesHeading>
  <RadixThemesBox css={{"@media screen and (min-width: 0)": {"display": "block"}, "@media screen and (min-width: 30em)": {"display": "none"}, "@media screen and (min-width: 48em)": {"display": "none"}, "@media screen and (min-width: 62em)": {"display": "none"}}}>
  <RadixThemesTabs.Root css={{"&[data-orientation='vertical']": {"display": "flex"}}} defaultValue={`tab1`} orientation={`vertical`}>
  <RadixThemesTabs.List className={`flex-col`} css={{"&[data-orientation='vertical']": {"display": "block", "boxShadow": "inset -1px 0 0 0 var(--gray-a5)"}}}>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab1`}>
  {`SINCERIDAD`}
</RadixThemesTabs.Trigger>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab2`}>
  {`DEPRESIÓN`}
</RadixThemesTabs.Trigger>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab3`}>
  {`NEUROTICISMO`}
</RadixThemesTabs.Trigger>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab4`}>
  {`PSICOPATÍA`}
</RadixThemesTabs.Trigger>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab5`}>
  {`PSICOTICISMO`}
</RadixThemesTabs.Trigger>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab6`}>
  {`PARANOIDISMO`}
</RadixThemesTabs.Trigger>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab7`}>
  {`EXTRAVERSIÓN`}
</RadixThemesTabs.Trigger>
</RadixThemesTabs.List>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab1`}>
  <RadixThemesText as={`p`}>
  {`En el test encontrarás algunas preguntas que están encaminadas a comprobar si tiendes a falsear 
tus respuestas porque te parezcan que son socialmente más aceptables en vez responder la opción que realmente 
refleja tu personalidad. Generalmente son preguntas sobre actividades que realizas con frecuencia.`}
</RadixThemesText>
</RadixThemesTabs.Content>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab2`}>
  <RadixThemesText as={`p`}>
  {`También realizan preguntas que pretenden valorar si tienes alterada la capacidad para captar, sentir 
y manifestar los afectos. Quieren comprobar que no estás deprimido. Si lo estás tendrás signos y síntomas como 
pueden ser retraimiento, apatía o ideas delirantes, irritabilidad, ansiedad, dificultad en las relaciones… incluso 
también síntomas físicos.`}
</RadixThemesText>
</RadixThemesTabs.Content>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab3`}>
  <RadixThemesText as={`p`}>
  {`Esta dimensión es fundamental en la personalidad y todos la tenemos en algún grado es la que controla cómo 
respondes a los estímulos externos y cómo reaccionas a los problemas. En el test hay preguntas que valoran tu estabilidad emocional.`}
</RadixThemesText>
</RadixThemesTabs.Content>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab4`}>
  <RadixThemesText as={`p`}>
  {`La psicopatía o personalidad psicopática es un trastorno antisocial de la personalidad que se caracteriza por falta de empatía, 
pobre control de los impulsos y conductas manipulativas. En el test buscarán si tienes tus propios códigos de conducta y te alejas de las 
normas sociales comunes o si sientes las emociones como el resto de las personas, tienes remordimientos, proporcionalidad y empatía.`}
</RadixThemesText>
</RadixThemesTabs.Content>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab5`}>
  <RadixThemesText as={`p`}>
  {`Esta dimensión comprueba tu vulnerabilidad a conductas impulsivas, agresivas o de baja empatía. Comprueban, en función de tus 
respuestas, si tienes una mentalidad desconsiderada, imprudente, hostil, irascible, irracional o impulsiva. Si sientes agrado por sensaciones 
físicas muy fuertes o crueldad inhumana.`}
</RadixThemesText>
</RadixThemesTabs.Content>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab6`}>
  <RadixThemesText as={`p`}>
  {`También comprobarán si tienes un trastorno delirante,  estos trastornos producen un quiebro de la realidad y el enfermo crea una 
nueva dentro de su mente en la que se siente víctima de las acciones de una o varias personas o de una institución, creyendo que actúan en su 
contra y siendo imposible convencerlo de lo contrario por medio de la lógica.`}
</RadixThemesText>
</RadixThemesTabs.Content>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab7`}>
  <RadixThemesText as={`p`}>
  {`Este rasgo podemos definirlo como el deseo y la facilidad que tenemos de contactar con otras, en el test habrá también preguntas 
destinadas a valorar el grado de introversión o extraversión que tienes.`}
</RadixThemesText>
</RadixThemesTabs.Content>
</RadixThemesTabs.Root>
</RadixThemesBox>
  <RadixThemesBox css={{"align": "center", "@media screen and (min-width: 0)": {"display": "none"}, "@media screen and (min-width: 30em)": {"display": "block"}, "@media screen and (min-width: 48em)": {"display": "block"}, "@media screen and (min-width: 62em)": {"display": "block"}}}>
  <RadixThemesTabs.Root css={{"&[data-orientation='vertical']": {"display": "flex"}}} defaultValue={`tab1`}>
  <RadixThemesTabs.List css={{"&[data-orientation='vertical']": {"display": "block", "boxShadow": "inset -1px 0 0 0 var(--gray-a5)"}}}>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab1`}>
  {`SINCERIDAD`}
</RadixThemesTabs.Trigger>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab2`}>
  {`DEPRESIÓN`}
</RadixThemesTabs.Trigger>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab3`}>
  {`NEUROTICISMO`}
</RadixThemesTabs.Trigger>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab4`}>
  {`PSICOPATÍA`}
</RadixThemesTabs.Trigger>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab5`}>
  {`PSICOTICISMO`}
</RadixThemesTabs.Trigger>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab6`}>
  {`PARANOIDISMO`}
</RadixThemesTabs.Trigger>
  <RadixThemesTabs.Trigger css={{"&[data-orientation='vertical']": {"width": "100%"}}} value={`tab7`}>
  {`EXTRAVERSIÓN`}
</RadixThemesTabs.Trigger>
</RadixThemesTabs.List>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab1`}>
  <RadixThemesText as={`p`}>
  {`En el test encontrarás algunas preguntas que están encaminadas a comprobar si tiendes a falsear 
tus respuestas porque te parezcan que son socialmente más aceptables en vez responder la opción que realmente 
refleja tu personalidad. Generalmente son preguntas sobre actividades que realizas con frecuencia.`}
</RadixThemesText>
</RadixThemesTabs.Content>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab2`}>
  <RadixThemesText as={`p`}>
  {`También realizan preguntas que pretenden valorar si tienes alterada la capacidad para captar, sentir 
y manifestar los afectos. Quieren comprobar que no estás deprimido. Si lo estás tendrás signos y síntomas como 
pueden ser retraimiento, apatía o ideas delirantes, irritabilidad, ansiedad, dificultad en las relaciones… incluso 
también síntomas físicos.`}
</RadixThemesText>
</RadixThemesTabs.Content>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab3`}>
  <RadixThemesText as={`p`}>
  {`Esta dimensión es fundamental en la personalidad y todos la tenemos en algún grado es la que controla cómo 
respondes a los estímulos externos y cómo reaccionas a los problemas. En el test hay preguntas que valoran tu estabilidad emocional.`}
</RadixThemesText>
</RadixThemesTabs.Content>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab4`}>
  <RadixThemesText as={`p`}>
  {`La psicopatía o personalidad psicopática es un trastorno antisocial de la personalidad que se caracteriza por falta de empatía, 
pobre control de los impulsos y conductas manipulativas. En el test buscarán si tienes tus propios códigos de conducta y te alejas de las 
normas sociales comunes o si sientes las emociones como el resto de las personas, tienes remordimientos, proporcionalidad y empatía.`}
</RadixThemesText>
</RadixThemesTabs.Content>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab5`}>
  <RadixThemesText as={`p`}>
  {`Esta dimensión comprueba tu vulnerabilidad a conductas impulsivas, agresivas o de baja empatía. Comprueban, en función de tus 
respuestas, si tienes una mentalidad desconsiderada, imprudente, hostil, irascible, irracional o impulsiva. Si sientes agrado por sensaciones 
físicas muy fuertes o crueldad inhumana.`}
</RadixThemesText>
</RadixThemesTabs.Content>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab6`}>
  <RadixThemesText as={`p`}>
  {`También comprobarán si tienes un trastorno delirante,  estos trastornos producen un quiebro de la realidad y el enfermo crea una 
nueva dentro de su mente en la que se siente víctima de las acciones de una o varias personas o de una institución, creyendo que actúan en su 
contra y siendo imposible convencerlo de lo contrario por medio de la lógica.`}
</RadixThemesText>
</RadixThemesTabs.Content>
  <RadixThemesTabs.Content css={{"&[data-orientation='vertical']": {"width": "100%", "margin": null}, "padding": "8px"}} value={`tab7`}>
  <RadixThemesText as={`p`}>
  {`Este rasgo podemos definirlo como el deseo y la facilidad que tenemos de contactar con otras, en el test habrá también preguntas 
destinadas a valorar el grado de introversión o extraversión que tienes.`}
</RadixThemesText>
</RadixThemesTabs.Content>
</RadixThemesTabs.Root>
</RadixThemesBox>
</RadixThemesFlex>
</RadixThemesBox>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`column`} gap={`3`}>
  <Button_2ea5f7b2c7e7d19f5ba3578d44899189/>
</RadixThemesFlex>
</RadixThemesFlex>
</RadixThemesFlex>
  <RadixThemesFlex align={`center`} className={`rx-Stack`} css={{"margin": "1em"}} direction={`column`} gap={`3`}>
  <RadixThemesFlex align={`start`} className={`rx-Stack`} direction={`row`} gap={`3`}>
  <Link_0c4255b4db2c5f3b9f3a676146b5ba1e/>
</RadixThemesFlex>
</RadixThemesFlex>
</RadixThemesBox>
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

const pulse = keyframes`
    0% {
        opacity: 0;
    }
    100% {
        opacity: 1;
    }
`


export function Button_2ea5f7b2c7e7d19f5ba3578d44899189 () {
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  const on_click_fd35fdea558f9c471def5d85fa21c55a = useCallback((_e) => addEvents([Event("_redirect", {path:`/test`,external:false,replace:false})], (_e), {}), [addEvents, Event])


  return (
    <RadixThemesButton css={{"padding": "1em", "borderRadius": "0", "backgroundColor": ["#FC4F00"], "&:hover": {"backgroundColor": ["#1B9AAF"]}}} onClick={on_click_fd35fdea558f9c471def5d85fa21c55a} size={`3`}>
  {`Comenzar test`}
</RadixThemesButton>
  )
}

export function Box_d7908424bebc27ea2f94eab62d6a3dd6 () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <RadixThemesBox css={{"backgroundColor": isTrue(((colorMode) === (`light`))) ? `#FBE6CC` : ["#B2B2B2"], "borderRadius": "3px", "padding": "8px", "width": "100%", "textAlign": "center"}}>
  {`ALGUNAS VECES`}
</RadixThemesBox>
  )
}

export function Box_1d145a476a1e8d09efc39ace50d76e4a () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <RadixThemesBox css={{"backgroundColor": isTrue(((colorMode) === (`light`))) ? `#FBE6CC` : ["#B2B2B2"], "borderRadius": "3px", "padding": "8px", "width": "100%", "textAlign": "center"}}>
  {`POCAS VECES`}
</RadixThemesBox>
  )
}

export function Box_e4f74c0124d5bac2bd1a273bceec6a1e () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <RadixThemesBox css={{"backgroundColor": isTrue(((colorMode) === (`light`))) ? `#FBE6CC` : ["#B2B2B2"], "borderRadius": "3px", "padding": "8px", "width": "100%", "textAlign": "center"}}>
  {`NO`}
</RadixThemesBox>
  )
}

export function Box_045dd26aef07260269fa66f5fc35475c () {
  const [ colorMode, toggleColorMode ] = useContext(ColorModeContext)



  return (
    <RadixThemesBox css={{"backgroundColor": isTrue(((colorMode) === (`light`))) ? `#FBE6CC` : ["#B2B2B2"], "borderRadius": "3px", "padding": "8px", "width": "100%", "textAlign": "center"}}>
  {`MUCHAS VECES`}
</RadixThemesBox>
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

export function Link_0c4255b4db2c5f3b9f3a676146b5ba1e () {



  return (
    <RadixThemesLink asChild={true} css={{"textDecoration": "none", "&:hover": {"color": "var(--accent-8)"}, "color": ["#FC4F00"], "paddingBottom": "15px", "textAlign": "center"}} size={`2`} target={isTrue(true) ? `_blank` : ``}>
  <NextLink href={`https://academiametodos.com/`} passHref={true}>
  {`© 2015-2026 Métodos Centro de Formación Integral S.L.U.`}
</NextLink>
</RadixThemesLink>
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

export default function Component() {

  return (
    <Fragment>
  <Fragment>
  <Div_ac2a89ea84667d600a059f034bd91dfe/>
  <Toaster_89416713a273995fc60191a4cf573054/>
</Fragment>
  <Box_0f698ff7a7a3cb7838146be9a5c5e574/>
  <NextHead>
  <title>
  {`Info`}
</title>
  <meta content={`favicon.ico`} property={`og:image`}/>
</NextHead>
</Fragment>
  )
}
