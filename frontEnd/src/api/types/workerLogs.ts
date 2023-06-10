export type LoginParam = Partial<{
  username: string | undefined;
  password: string | undefined;
}> | null;

export type LoginResponse = Partial<{
  role: string | undefined;
  access_token: string | undefined;
}>;
