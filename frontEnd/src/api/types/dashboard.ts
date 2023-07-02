export type dashInfo = Partial<{
    user_total: string | undefined;
    system_info: string | undefined;
    logger_total: string | undefined;
    project_total: string | undefined;
    master_cpu: string | undefined;
}> | null;
