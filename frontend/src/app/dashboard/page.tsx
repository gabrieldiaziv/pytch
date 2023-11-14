// "use client";
import { getServerSession } from "next-auth";
import { authOptions } from "@/server/auth";
// import React, { useEffect, useState } from 'react';


export default async function UserPage() {
  const url = "https://s3.us-east-2.amazonaws.com/joeyquismor.io/iris_scatter_plot.html";
  const session = await getServerSession(authOptions);

  return (
    <div className="flex flex-col w-full h-[100svh]">
      <div className="flex w-full h-[10%]">

      </div>
      <div className="flex w-full h-[90%]">
        <div className="flex flex-col w-full h-1/2 p-4 gap-6">
          <h1 className="text-3xl font-semibold">Dashboard</h1>
          <div>
          {/* <iframe 
            src={url} 
            title="HTML Content" 
            width="100%" 
            height="600px" 
            style={{ border: 'none' }}
        /> */}
          </div>
          <div className="flex h-full">
          </div>
        </div>
      </div>
    </div>
  );
}
