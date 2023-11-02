import * as q from "../queries";

export default class UserService {
  static async createUser(id: string, username: string) {
    await q.createUser(id, username);
  }

  static async getUserById(id: string) {
    return await q.getUserById(id);
  }
}
