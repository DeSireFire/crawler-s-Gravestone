export type alarmers = Partial<{
    id: number | undefined;
    name: string | undefined,
    email: string | undefined,
    qw_token: string | undefined,
    resource: string | undefined,
    desc: string | undefined,
    create_time: string | undefined;
    update_time: string | undefined;
}> | null;


export type alarm_jobs = Partial<{
    id: number | undefined;
    pid: string | undefined,
    wid: string | undefined,
    name: string | undefined,
    email: string | undefined,
    qw_token: string | undefined,
    resource: string | undefined,
    desc: string | undefined,
    alarm_content: string | undefined,
    create_time: string | undefined;
    update_time: string | undefined;
}> | null;
