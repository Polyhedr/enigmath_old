// pages/index.tsx
import type { NextPage } from "next";
import Head from "next/head";
import Image from "next/image";
import { useEffect, useRef, useState } from "react";
import getBase64ImageUrl from "../utils/generateBlurPlaceholder";
import type { ImageProps } from "../utils/types";
import { useLastViewedPhoto } from "../utils/useLastViewedPhoto";
import getResults from "../utils/cachedImages";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";

interface EnigmaData {
  src: string;
  text: string;
  folderName: string;
  title: string;
}

const Home: NextPage<{ images: ImageProps[] }> = ({ images }) => {
  const [lastViewedPhoto, setLastViewedPhoto] = useLastViewedPhoto();
  const lastViewedPhotoRef = useRef<HTMLDivElement>(null);
  const overlayRef = useRef<HTMLDivElement>(null);

  const [activeEnigma, setActiveEnigma] = useState<EnigmaData | null>(null);
  const [downloading, setDownloading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [searchQuery, setSearchQuery] = useState("");

  // ---------------- Download solution ----------------
  const triggerDownload = (blob: Blob, filename: string) => {
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
    URL.revokeObjectURL(link.href);
  };

  const downloadSolution = async () => {
    if (!activeEnigma) return;

    setDownloading(true);
    setProgress(0);

    const folder = activeEnigma.folderName;
    const isIntro = folder === "Introduction";
    const url = isIntro
      ? `/Introduction/template.zip`
      : `/enigmas/${encodeURIComponent(folder)}/solution.pdf`;

    const response = await fetch(url);
    const total = Number(response.headers.get("Content-Length"));

    if (!response.body) {
      const blob = await response.blob();
      triggerDownload(blob, isIntro ? "template.zip" : `${folder}-solution.pdf`);
      setDownloading(false);
      return;
    }

    const reader = response.body.getReader();
    let received = 0;
    const chunks: Uint8Array[] = [];

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      chunks.push(value);
      received += value.length;
      setProgress(Math.round((received / total) * 100));
    }

    const blob = new Blob(chunks, { type: isIntro ? "application/zip" : "application/pdf" });
    triggerDownload(blob, isIntro ? "template.zip" : `${folder}-solution.pdf`);

    setDownloading(false);
    setProgress(100);
  };

  // ---------------- Load an enigma ----------------
  const loadEnigma = async (folderName: string) => {
    if (!folderName) return;

    try {
      const basePath =
        folderName === "Introduction"
          ? `/${encodeURIComponent(folderName)}`
          : `/enigmas/${encodeURIComponent(folderName)}`;

      const textResponse = await fetch(`${basePath}/text.md`);
      const text = await textResponse.text();

      const srcJpg = `${basePath}/image.jpg`;
      const srcPng = `${basePath}/image.png`;

      const src =
        (await fetch(srcJpg, { method: "HEAD" }).then(res => res.ok).catch(() => false))
          ? srcJpg
          : srcPng;

      // find preloaded image data
      const preloaded = images.find(img => img.folderName === folderName);

      setActiveEnigma({
        src,
        text,
        folderName,
        title: preloaded?.title || folderName,
      });

      window.history.pushState({ enigma: folderName }, "", `#${encodeURIComponent(folderName)}`);
    } catch (err) {
      console.error("Failed to load enigma:", err);
    }
  };


  // ---------------- Open from URL hash ----------------
  useEffect(() => {
    const hash = decodeURIComponent(window.location.hash.replace("#", ""));
    if (hash) {
      loadEnigma(hash);
    }
  }, []);

  // ---------------- Overlay / body scroll management ----------------
  useEffect(() => {
    if (activeEnigma) {
      document.body.style.overflow = "hidden";
      overlayRef.current?.scrollTo({ top: 0, behavior: "auto" });
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [activeEnigma]);

  // ---------------- Back navigation ----------------
  useEffect(() => {
    const handlePopState = () => setActiveEnigma(null);
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  // ---------------- Scroll to last viewed photo ----------------
  useEffect(() => {
    if (lastViewedPhoto && activeEnigma === null) {
      lastViewedPhotoRef.current?.scrollIntoView({ block: "center" });
      setLastViewedPhoto(null);
    }
  }, [activeEnigma, lastViewedPhoto, setLastViewedPhoto]);

  const closeEnigma = () => {
    setActiveEnigma(null);
    if (window.location.hash) window.history.back();
  };

  // ---------------- Filter images ----------------
  const filteredImages = images.filter((img) => {
    const query = searchQuery.toLowerCase();
    const titleMatch = img.title?.toLowerCase().includes(query) ?? false;
    const tagsMatch = img.tags?.some((tag) => tag.toLowerCase().includes(query)) ?? false;
    return titleMatch || tagsMatch;
  });

  return (
    <>
      <Head>
        <title>Enigmath</title>
      </Head>

      <main className="mx-auto max-w-[1960px] p-4">
        {/* ---------------- Header + Search ---------------- */}
        <div className="mb-4 flex items-center gap-3">
          {/* Logo */}
          <div
            onClick={() => loadEnigma("Introduction")}
            className="h-16 aspect-[2/1] relative overflow-hidden rounded cursor-pointer group transition"
          >
            <div className="absolute inset-0 pointer-events-none bg-transparent group-hover:bg-white/25 transition" />
            <div
              className="h-full w-full bg-[rgb(255,255,255)]"
              style={{
                WebkitMaskImage: "url('/Introduction/logo.svg')",
                maskImage: "url('/Introduction/logo.svg')",
                WebkitMaskSize: "contain",
                maskSize: "contain",
                WebkitMaskRepeat: "no-repeat",
                maskRepeat: "no-repeat",
                WebkitMaskPosition: "center",
                maskPosition: "center",
              }}
            />
          </div>

          {/* Search */}
          <input
            type="text"
            placeholder="Rechercher..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded h-12"
          />
        </div>

        {/* ---------------- Gallery ---------------- */}
        <div className="grid gap-4 grid-cols-[repeat(auto-fill,minmax(250px,1fr))]">
          {filteredImages
            .sort((a, b) => a.folderName.localeCompare(b.folderName))
            .map((img) => (
              <div
                key={img.id}
                ref={img.folderName && img.id === Number(lastViewedPhoto) ? lastViewedPhotoRef : null}
                className="relative mb-5 cursor-pointer rounded-lg overflow-hidden shadow-md group"
                onClick={() => img.folderName && loadEnigma(img.folderName)}
              >
<div className="absolute top-0 left-0 right-0 bg-black/60 text-white py-2 px-3 z-10">
  <div className="relative">

{/* Top-right indicators */}
<div className="absolute top-0 right-0 flex gap-2 whitespace-nowrap text-sm font-semibold">
  {typeof img.difficulty === "number" && (
    <span className="text-red-300">
      🌶️<sup>{img.difficulty.toFixed(1)}</sup>
    </span>
  )}
  {typeof img.computer === "number" && (
    <span className="text-blue-300">
      💻<sup>{img.computer.toFixed(1)}</sup>
    </span>
  )}
</div>

    {/* Title with padding to avoid overlap */}
    <div className="pr-28 text-lg font-semibold leading-tight line-clamp-2">
      {img.title}
    </div>

  </div>
</div>
                <div className="absolute bottom-0 left-0 right-0 p-1 flex flex-wrap gap-1 bg-black/40 text-white text-xs z-10">
                  {img.tags?.map((tag) => (
                    <span key={tag} className="px-2 py-0.5 bg-white/20 rounded-full backdrop-blur-sm">
                      {tag}
                    </span>
                  ))}
                </div>
                <Image
                  alt={`Photo ${img.id}`}
                  src={img.src}
                  placeholder="blur"
                  blurDataURL={img.blurDataUrl}
                  width={720}
                  height={720}
                  className="transform rounded-lg brightness-90 transition group-hover:brightness-110 object-cover"
                />
              </div>
            ))}
        </div>
      </main>

      {/* ---------------- Overlay ---------------- */}
      {activeEnigma && (
        <div
          ref={overlayRef}
          className="fixed inset-0 z-50 bg-white text-black overflow-y-auto"
        >
          {/* Header */}
          <div className="fixed top-0 left-0 right-0 z-50 flex justify-between items-center p-4 gap-4 border-b bg-white border-gray-300">
            <h2 className="text-lg font-semibold">{activeEnigma.title}</h2>
            <div className="flex gap-2">
              
              {/* Download */}
          <div className="relative w-12 h-12 flex items-center justify-center">
            <button
              onClick={downloadSolution}
              disabled={downloading}
              className={`w-12 h-12 flex items-center justify-center 
                ${
                  downloading ? "bg-gray-400" : "bg-green-500 hover:bg-green-600"
                } text-white rounded-full font-bold transition text-2xl`}
              title={
                activeEnigma.folderName === "Introduction"
                  ? "Télécharger le template"
                  : "Télécharger la solution"
              }
            >
              ⤓
            </button>

            {downloading && (
              <div className="absolute inset-0 flex items-center justify-center">
                <svg
                  className="animate-spin text-white"
                  width="32"
                  height="32"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="white"
                    strokeWidth="4"
                    fill="none"
                  />
                  <path
                    className="opacity-75"
                    fill="white"
                    d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                  />
                </svg>
              </div>
            )}
          </div>

              {/* Mail */}
              <a
                href={`mailto:contact.enigmath@gmail.com?subject=${encodeURIComponent(
                  activeEnigma.folderName
                )}&body=${
                  activeEnigma.folderName === "Introduction"
                    ? "Voici mon énigme :"
                    : "Voici ma réponse à la question X :"
                }`}
                className="w-12 h-12 flex items-center justify-center bg-blue-500 hover:bg-blue-600 text-white rounded font-semibold transition text-2xl"
                title={
                  activeEnigma.folderName === "Introduction"
                    ? "Soumettre une énigme"
                    : "Soumettre une question/réponse"
                }
              >
                ➤
              </a>

              {/* Close */}
              <button
                onClick={closeEnigma}
                className="w-12 h-12 flex items-center justify-center bg-gray-200 hover:bg-gray-300 rounded text-gray-700 font-semibold transition text-2xl"
                title="Fermer"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Scrollable content */}
          <div className="pt-28 max-w-4xl mx-auto px-6 py-8 flex flex-col gap-6">
            {/* Image */}
            <div className="flex-shrink-0 mx-auto">
              {activeEnigma.folderName === "Introduction" ? (
                <img src="/Introduction/logo.svg" alt="Logo" className="h-32 w-auto object-contain" />
              ) : (
                <Image
                  alt="Selected photo"
                  src={activeEnigma.src}
                  width={320}
                  height={320}
                  className="rounded-lg object-contain shadow-md"
                  placeholder="blur"
                />
              )}
            </div>

            {/* Markdown */}
            <div className="markdown-body w-full break-words whitespace-normal overflow-x-auto">
              <ReactMarkdown
                remarkPlugins={[remarkGfm, remarkMath]}
                rehypePlugins={[rehypeKatex]}
                components={{
                  ol: ({ node, ...props }) => <ol className="list-decimal ml-6 space-y-3" {...props} />,
                  li: ({ node, ...props }) => <li className="leading-relaxed" {...props} />,
                  p: ({ node, ...props }) => <p className="mb-3" {...props} />,
                }}
              >
                {activeEnigma.text}
              </ReactMarkdown>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Home;

export async function getStaticProps() {
  const localImages = await getResults();

  const images: ImageProps[] = await Promise.all(
    localImages.map(async (img) => {
      let title = img.folderName;
      let difficulty: number | undefined;
      let computer: number | undefined;
      let tags: string[] = [];

      try {
        const tagsPath =
          img.folderName === "Introduction"
            ? path.join(process.cwd(), "public", "Introduction", "tags.txt")
            : path.join(process.cwd(), "public", "enigmas", img.folderName, "tags.txt");

        const raw = await fs.readFile(tagsPath, "utf-8");

        const parts = raw
          .split(/[\n,]/)
          .map(t => t.trim())
          .filter(Boolean);

        difficulty = Number(parts[0]) || undefined;
        computer = Number(parts[1]) || undefined;
        title = parts[2] || img.folderName;
        tags = parts.slice(3);
      } catch {
        console.warn(`No tags.txt for ${img.folderName}`);
      }

      return {
        ...img,
        title,
        difficulty,
        computer,
        tags,
        blurDataUrl: await getBase64ImageUrl(img),
      };
    })
  );

  return { props: { images } };
}


