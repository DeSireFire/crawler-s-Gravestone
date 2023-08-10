export type program = Partial<{
    id: string | undefined;
    // code id
    cid: string | undefined;
    name: string | undefined;
    git_repo: string | undefined;
    base_path: string | undefined;
    repo_path: string | undefined;
    shell: string | undefined;
    requirements: string | undefined;
    interpreter: string | undefined;
    description: string | undefined;
    author: string | undefined;
    extra: string | undefined;
    create_time: string | undefined;
    update_time: string | undefined;
}> | null;
