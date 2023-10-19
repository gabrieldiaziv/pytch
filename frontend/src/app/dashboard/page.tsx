import { getServerSession } from "next-auth";
import { authOptions } from "@/server/auth";
import Header from "../_components/header";


export default async function UserPage() {
  const session = await getServerSession(authOptions);

  return (
    <div className="flex flex-col w-full h-[100svh]">
      <div className="flex w-full h-[10%]">
        <Header />
      </div>
      <div className="flex w-full h-[90%]">
        <div className="flex flex-col w-full h-1/2 p-4 gap-6">
          <h1 className="text-3xl font-semibold">My Shows</h1>
          <div className="flex h-full">
          </div>
        </div>
      </div>
    </div>
  );
}
