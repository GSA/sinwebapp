export interface User{
    id: number,
    email: string;
    groups: string[];
}

export const GROUPS = {
    submitter: 'submitter_group',
    reviewer: 'reviewer_group',
    approver: 'approver_group',
    admin: 'admin_group'
}

export const null_User : User ={
    id: null,
    email: null,
    groups: null
}