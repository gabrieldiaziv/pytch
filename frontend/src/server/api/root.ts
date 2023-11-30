import { createTRPCRouter } from "@/server/api/trpc";
import { matchRouter } from "./routers/match";

/**
 * This is the primary router for your server.
 *
 * All routers added in /api/routers should be manually added here.
 */
export const appRouter = createTRPCRouter({
  match: matchRouter,
});

// export type definition of API
export type AppRouter = typeof appRouter;
