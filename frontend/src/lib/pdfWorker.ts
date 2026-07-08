import { pdfjs } from "react-pdf";

// react-pdf needs pdf.js's worker script. Loading it from a CDN avoids extra
// bundler config; pin the version to whatever react-pdf resolves at build time.
pdfjs.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;
