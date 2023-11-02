import { PrismaAdapter } from "@next-auth/prisma-adapter";
import {
  getServerSession,
  type DefaultSession,
  type NextAuthOptions,
} from "next-auth";
import Auth0Provider, { type Auth0Profile } from "next-auth/providers/auth0";

import { env } from "@/env.mjs";
import { db } from "@/server/db";
import { getBaseUrl } from "@/utils";
import { type Role } from "@prisma/client";
import UserService from "./service/user";

/**
 * Module augmentation for `next-auth` types. Allows us to add custom properties to the `session`
 * object and keep type safety.
 *
 * @see https://next-auth.js.org/getting-started/typescript#module-augmentation
 */
declare module "next-auth" {
  interface Session extends DefaultSession {
    user: {
      id: string;
      type: Role;
      username: string;
      displayName: string;
    } & DefaultSession["user"];
  }

  interface Profile extends Auth0Profile {
    email_verified: boolean; // from user stored in Auth0
  }
}

/**
 * Options for NextAuth.js used to configure adapters, providers, callbacks, etc.
 *
 * @see https://next-auth.js.org/configuration/options
 */
export const authOptions: NextAuthOptions = {
  session: {
    strategy: "jwt",
  },
  callbacks: {
    redirect({ url, baseUrl }) {
      if (url === "/api/auth/signin") {
        return `${baseUrl}/dashboard`;
      }

      if (url === "/api/auth/signout") {
        return `${baseUrl}`;
      }

      return url;
    },
    jwt: async ({ trigger, user, token, profile }) => {
      if (trigger === "signUp") {
        // create new user in database
        await UserService.createUser(user.id, user.name ?? "");
      }

      if (user) {
        if (profile) {
          // check if email is verified from Auth0
          token.email_verified = profile.email_verified;
        }
        if (token.email_verified) {
          // get existing user
          const dbUser = await UserService.getUserById(user.id);
          if (dbUser) {
            token.userId = dbUser.id;
            token.userType = dbUser.type;
            token.username = dbUser.username;
            token.displayName = dbUser.display_name;
          }
        }
      }

      return token;
    },
    session({ session, token }) {
      session = {
        ...session,
        user: {
          ...session.user,
          id: String(token.userId),
          type: token.userType as Role,
          username: String(token.username),
          displayName: String(token.displayName),
        },
      };

      return session;
    },
  },

  adapter: PrismaAdapter(db),
  providers: [
    Auth0Provider({
      clientId: env.AUTH0_CLIENT_ID,
      clientSecret: env.AUTH0_CLIENT_SECRET,
      issuer: env.AUTH0_ISSUER,
      authorization: {
        params: {
          scope: "openid profile email offline_access",
          prompt: "login",
          redirect_uri: getBaseUrl() + "/api/auth/callback/auth0",
          response_type: "code",
        },
      },
    }),

    /**
     * ...add more providers here.
     *
     * Most other providers require a bit more work than the Discord provider. For example, the
     * GitHub provider requires you to add the `refresh_token_expires_in` field to the Account
     * model. Refer to the NextAuth.js docs for the provider you want to use. Example:
     *
     * @see https://next-auth.js.org/providers/github
     */
  ],
  pages: {
    signIn: "/auth/signin",
    signOut: "/auth/signout",
    error: "/auth/error", // Error code passed in query string as ?error=
  },
  secret: env.NEXTAUTH_SECRET,
};

/**
 * Wrapper for `getServerSession` so that you don't need to import the `authOptions` in every file.
 *
 * @see https://next-auth.js.org/configuration/nextjs
 */
export const getServerAuthSession = () => getServerSession(authOptions);
