export type alarmers = Partial<{
    id: number | undefined;
    aid: string | undefined;
    name: string | undefined,
    email: string | undefined,
    qw_token: string | undefined,
    resource: string | undefined,
    desc: string | undefined,
    extra: string | undefined;
    create_time: string | undefined;
}> | null;


export type alarm_jobs = Partial<{
    id: number | undefined;
    a_jid: string | undefined,
    wid: string | undefined,
    aid: string | undefined,
    name: string | undefined,
    delivery: number | undefined,
    resource: string | undefined,
    desc: string | undefined,
    alarm_content: string | undefined,
    extra: string | undefined;
    create_time: string | undefined;
}> | null;
