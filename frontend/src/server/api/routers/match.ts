import { createTRPCRouter, protectedProcedure, publicProcedure } from "../trpc";

export const userRouter = createTRPCRouter({
  flaskTest: protectedProcedure.query(({ ctx }) => {
    console.log(ctx.session.accessToken);
  }),
});
