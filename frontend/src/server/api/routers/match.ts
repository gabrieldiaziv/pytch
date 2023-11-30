import { z } from "zod";
import { createTRPCRouter, protectedProcedure } from "../trpc";

export const matchRouter = createTRPCRouter({
  getVizs: protectedProcedure
    .input(z.object({ matchId: z.string() }))
    .query(async ({ input, ctx }) => {
      const vizs = await ctx.db.viz.findMany({
        where: {
          match_id: {
            equals: input.matchId,
          },
        },
      });

      return vizs;
    }),

  insertMatch: protectedProcedure
    .input(z.object({ matchId: z.string(), matchName: z.string(), matchDate: z.date(), team1Name: z.string(), team2Name: z.string() }))
    .mutation(async ({ input, ctx }) => {
      const match = await ctx.db.gameMatch.create({
        data: {
          match_id: input.matchId,
          name: input.matchName,
          date: input.matchDate,
          team1Name: input.team1Name,
          team2Name: input.team2Name,
          user_id: ctx.session.user.id,
        },
      });

      return match;
    }),

  getUserMatches: protectedProcedure
    .query(async ({ ctx }) => {
      const matches = await ctx.db.gameMatch.findMany({
        where: {
          user_id: {
            equals: ctx.session.user.id,
          },
        },
      });

      return matches;
    }),
    
  getMatch: protectedProcedure
    .input(z.object({ matchId: z.string() }))
    .query(async ({ input, ctx }) => {
      const match = await ctx.db.gameMatch.findUnique({
        where: {
          match_id: input.matchId,
        },
      });

      return match;
    }),

  deleteMatch: protectedProcedure
    .input(z.object({ matchId: z.string() }))
    .mutation(async ({ input, ctx }) => {
      const match = await ctx.db.gameMatch.delete({
        where: {
          match_id: input.matchId,
        },
      });

      return match;
    }),
});
