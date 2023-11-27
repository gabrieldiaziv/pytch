import { NextResponse } from "next/server";

import { db } from "@/server/db";

export async function GET(req: Request, { params }: { params: { id: string } }) {
  try {
    const match = await db.gameMatch.findUnique({
        where: {
            match_id: params.id
          }
        });

    return NextResponse.json({ match: match });
  } catch (error) {
    console.error(error);
    return NextResponse.json({ error: error });
  }
}