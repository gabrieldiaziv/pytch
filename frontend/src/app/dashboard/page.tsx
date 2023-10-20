import { getServerSession } from "next-auth";
import { authOptions } from "@/server/auth";


export default async function UserPage() {
  const session = await getServerSession(authOptions);

  return (
    <div className="flex flex-col w-full h-[100svh]">
      <div className="flex w-full h-[10%]">

      </div>
      <div className="flex w-full h-[90%]">
        <div className="flex flex-col w-full h-1/2 p-4 gap-6">
          <h1 className="text-3xl font-semibold">Dashboard view imma make this look good later but for now this gonna look like ass SKull EMoji</h1>
          <div>
          {JSON.stringify(session?.user, null, 2)}
          </div>
          <div className="flex h-full">
          </div>
        </div>
      </div>
    </div>
  );
}
