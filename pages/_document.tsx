import Document, { Head, Html, Main, NextScript } from "next/document";

class MyDocument extends Document {
  render() {
    return (
      <Html lang="en">
        <Head>

          {/* iOS settings */}
          <meta name="apple-mobile-web-app-capable" content="yes" />
          <meta name="apple-mobile-web-app-status-bar-style" content="black" />

          {/* FAVICONS */}
          <link rel="icon" href="/favicon.ico" />
          <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png" />
          <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png" />

          {/* ANDROID */}
          <link rel="icon" type="image/png" sizes="192x192" href="/android-chrome-192x192.png" />
          <link rel="icon" type="image/png" sizes="512x512" href="/android-chrome-512x512.png" />

          {/* iOS + Chrome iOS */}
          <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
          <link rel="icon" type="image/png" sizes="180x180" href="/apple-touch-icon.png" />

          {/* Manifest (ne pas changer le nom !) */}
          <link rel="manifest" href="/site.webmanifest?v=0" />

          <meta name="theme-color" content="#000000" />

          {/* tes metas */}
          <meta name="description" content="See pictures from Next.js Conf and the After Party." />
          <meta property="og:site_name" content="nextjsconf-pics.vercel.app" />
          <meta property="og:description" content="See pictures from Next.js Conf and the After Party." />
          <meta property="og:title" content="Next.js Conf 2022 Pictures" />
          <meta name="twitter:card" content="summary_large_image" />
          <meta name="twitter:title" content="Next.js Conf 2022 Pictures" />
          <meta name="twitter:description" content="See pictures from Next.js Conf and the After Party." />

        </Head>
        <body className="bg-black antialiased">
          <Main />
          <NextScript />
        </body>
      </Html>
    );
  }
}

export default MyDocument;
