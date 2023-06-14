export type DelLogData = Partial<{
  username: string | undefined;
  password: string | undefined;
  id:          number| undefined;
  name:        string| undefined;
  log_project: string| undefined;
  remarks:     string| undefined;
  address:     string| undefined;
}> | null;
