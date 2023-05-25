export const BASE_URL =
  process.env.NODE_ENV === "development"
    ? "http://api.cox.ink:6701"
    : "http://api.cox.ink:6701";

export enum ACCOUNT {
  LOGIN = "/auth_token",
}

export const API = {
  ACCOUNT,
};
