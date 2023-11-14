import { env } from "@/env.mjs";
import { JWKSchema } from "@/utils/z.schema";
import axios, { type AxiosRequestConfig } from "axios";
import jwt from "jsonwebtoken";
import * as q from "../queries";

export default class UserService {
  static async createUser(id: string, username: string) {
    await q.createUser(id, username);
  }

  static async getUserById(id: string) {
    return await q.getUserById(id);
  }

  static async verifyAccessToken(accessToken: string) {
    // get token headers

    const tokenHeaders = jwt.decode(accessToken, {
      complete: true,
    })?.header;

    if (!tokenHeaders || tokenHeaders.alg !== "RS256") {
      throw new Error("Invalid token headers");
    }

    const config: AxiosRequestConfig = {
      method: "get",
      maxBodyLength: Infinity,
      url: env.AUTH0_ISSUER + "/.well-known/jwks.json",
    };

    // get signing certificate from matching Auth0 JWK

    const JWKs = JWKSchema.parse((await axios.request(config)).data);
    const matchedJWK = JWKs.keys.find((jwk) => jwk.kid === tokenHeaders.kid);

    if (!matchedJWK?.x5c[0]) {
      throw new Error("No JWK found");
    }

    const certificate = `-----BEGIN CERTIFICATE-----\n${matchedJWK.x5c[0]}\n-----END CERTIFICATE-----`;

    // verify token
    const payload = jwt.verify(
      accessToken,
      certificate,
      {
        audience: env.AUTH0_CLIENT_ID,
        /**
         * @see https://stackoverflow.com/questions/49410108/auth0-authorizor-rejects-jwt-token-from-service-jwt-issuer-invalid-expected
         */
        issuer: env.AUTH0_ISSUER + "/",
        algorithms: ["RS256"],
      },
      (err) => {
        if (err) throw new Error(err.message);
      },
    );

    return payload;
  }
}
