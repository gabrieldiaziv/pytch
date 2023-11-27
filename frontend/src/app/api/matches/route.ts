import { NextResponse } from "next/server";

import { db } from "@/server/db";

export async function GET(req: Request) {
  try {
    const matches = await db.gameMatch.findMany();

    const serializedMatches = matches.map((match) => {
      return {match}
    });

    return NextResponse.json({ matches: serializedMatches });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: error });
  }
}