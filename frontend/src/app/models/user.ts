export interface User{
    id: number,
    email: string;
    groups: string[];
}

export const devUser : User = {
    id: -1,
    email: "devUser@gsa.gov",
    groups: ['admin_group']  
}

export const GROUPS = {
    submitter: 'submitter_group',
    reviewer: 'reviewer_group',
    approver: 'approver_group',
    admin: 'admin_group'
}