import { Prisma, type Role } from "@prisma/client";
import { db } from "./db";

export const createUser = async (
  id: string,
  username: string,
  type: Role = "USER",
) => {
  try {
    return await db.userData.create({
      data: {
        id,
        username: username,
        display_name: username,
        type: type,
      },
    });
  } catch (e) {
    if (e instanceof Prisma.PrismaClientKnownRequestError) {
      if (e.code === "P2002") {
        // TODO: username already exists, prompt user for another username in UI
        return await db.userData.create({
          data: {
            id,
            username: id, // set username to id for now
            display_name: username,
            type: "INITIAL_USER", 
          },
        });
      }
    }
  }
};

const getUserSelect = {
  id: true,
  username: true,
  display_name: true,
  type: true,
} satisfies Prisma.UserDataSelect;

export const getUserById = async (id: string) => {
  return await db.userData.findUnique({
    where: {
      id,
    },
    select: getUserSelect,
  });
};

export const getUserByName = async (username: string) => {
  return await db.userData.findUnique({
    where: {
      username,
    },
    select: getUserSelect,
  });
};
