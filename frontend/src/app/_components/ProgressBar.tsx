"use client"

import Router from "next/router";
import NProgress from "nprogress";
import "nprogress/nprogress.css";

NProgress.configure({
  minimum: 0.3,
  easing: "ease",
  speed: 800,
  showSpinner: false,
});

let progressBarScheduled: NodeJS.Timeout | undefined = undefined;
Router.events.on("routeChangeStart", () => {
  if (!progressBarScheduled) {
    progressBarScheduled = setTimeout(() => {
      progressBarScheduled = undefined;
      return NProgress.start();
    }, 120);
  }
});
Router.events.on("routeChangeComplete", () => {
  clearTimeout(progressBarScheduled);
  progressBarScheduled = undefined;
  return NProgress.done();
});
Router.events.on("routeChangeError", () => {
  clearTimeout(progressBarScheduled);
  progressBarScheduled = undefined;
  return NProgress.done();
});

export default function ProgressBar() {
  return null;
}