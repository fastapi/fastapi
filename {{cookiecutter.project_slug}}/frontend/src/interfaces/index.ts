export interface IUserProfile {
    admin_channels: string[];
    admin_roles: string[];
    disabled: boolean;
    email: string;
    human_name: string;
    name: string;
}

export interface IUserProfileUpdate {
    human_name?: string;
    password?: string;
    email?: string;
    admin_channels?: string[];
    admin_roles?: string[];
    disabled?: boolean;
}

export interface IUserProfileCreate {
    name: string;
    human_name?: string;
    password?: string;
    email?: string;
    admin_channels?: string[];
    admin_roles?: string[];
    disabled?: boolean;
}
