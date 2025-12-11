// pages/_app.tsx
import 'github-markdown-css/github-markdown.css';
import 'katex/dist/katex.min.css';
import type { AppProps } from 'next/app';
import "../styles/index.css";

function MyApp({ Component, pageProps }: AppProps) {
  return <Component {...pageProps} />;
}

export default MyApp;
