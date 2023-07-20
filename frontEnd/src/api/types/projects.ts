export type project = Partial<{
    id: number | undefined;
    nickname: string | undefined;
    name: string | undefined;
    description: string | undefined;
    pid: string | undefined;
    author: string | undefined;
    create_time: string | undefined;
    update_time: string | undefined;
}> | null;
