export type LoginParam = Partial<{
  username: string | undefined;
  password: string | undefined;
}> | null;

export type LoginResponse = Partial<{
  role: string | undefined;
  access_token: string | undefined;
}>;
// 获取用户列表
export type UsersResponse = Partial<{
  id: string | undefined;
  name: string | undefined;
  nicename: string | undefined;
  status: string | undefined;
  create: string | undefined;
  role: string | undefined;
  lastlogin: string | undefined;
  password: string | undefined;
}>;
//
// 获取用户列表
export type Person = Partial<{
  id: string | undefined;
  name: string | undefined;
  nicename: string | undefined;
  old_password: string | undefined;
  new_password: string | undefined;
}>;
