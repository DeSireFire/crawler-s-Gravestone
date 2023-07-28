export type project = Partial<{
    id: string | undefined;
    nickname: string | undefined;
    name: string | undefined;
    description: string | undefined;
    pid: string | undefined;
    author: string | undefined;
    create_time: string | undefined;
    update_time: string | undefined;
}> | null;

export type worker = Partial<{
    id: string | undefined;
    wid: string | undefined;
    pid: string | undefined;
    p_nickname: string | undefined;
    name: string | undefined;
    nickname: string | undefined;
    crawl_frequency: string | undefined;
    description: string | undefined;
    status: string | undefined;
    modify_user: string | undefined;
    extra: string | undefined;
    create_time: string | undefined;
    update_time: string | undefined;
}> | null;

export type job = Partial<{
    id: string | undefined;
    wid: string | undefined;
    pid: string | undefined;
    jid: string | undefined;
    p_nickname: string | undefined;
    w_nickname: string | undefined;
    name: string | undefined;
    status: string | undefined;
    run_user: string | undefined;
    log_file_path: string | undefined;
    log_lv_warning: string | undefined;
    log_lv_error: string | undefined;
    log_lv_info: string | undefined;
    log_lv_debug: string | undefined;
    items_count: string | undefined;
    extra: string | undefined;
    create_time: string | undefined;
    end_time: string | undefined;
}> | null;
