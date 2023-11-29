import { createTRPCRouter, protectedProcedure, publicProcedure } from "../trpc";
import {z} from 'zod';
import { db } from "@/server/db";

export const userRouter = createTRPCRouter({
  flaskTest: protectedProcedure.query(({ ctx }) => {
    console.log(ctx.session.accessToken);
  }),

  getVizs: protectedProcedure
    .input(z.object({matchId: z.string()}))
    .query(async ({input, ctx}) => {
      const vizs = await ctx.db.viz.findMany({
        where: {
          match_id: {
            equals: input.matchId,
          },
        },
      })

      return vizs
    })
});
