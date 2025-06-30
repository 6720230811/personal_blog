-- 创建个人博客数据库
CREATE DATABASE IF NOT EXISTS personal_blog CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 使用该数据库
USE personal_blog;

-- 创建 BlogOwner 表
CREATE TABLE IF NOT EXISTS BlogOwner (
    id INT NOT NULL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    avatar_url VARCHAR(255),
    github_url VARCHAR(255),
    github_username VARCHAR(50),
    bio TEXT,
    country VARCHAR(50),
    city VARCHAR(50),
    identity VARCHAR(100),
    last_login DATETIME
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 WorkExperience 表
CREATE TABLE IF NOT EXISTS WorkExperience (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    position VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE NOT NULL,
    end_date DATE,
    display_order INT NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 Education 表
CREATE TABLE IF NOT EXISTS Education (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    school_name VARCHAR(100) NOT NULL,
    major VARCHAR(100),
    degree VARCHAR(50),
    start_date DATE NOT NULL,
    end_date DATE,
    display_order INT NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 Achievement 表
CREATE TABLE IF NOT EXISTS Achievement (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    date DATE,
    location VARCHAR(100),
    display_order INT NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 Skill 表
CREATE TABLE IF NOT EXISTS Skill (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    proficiency INT NOT NULL,
    category VARCHAR(50),
    display_order INT NOT NULL DEFAULT 0,
    INDEX (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 Projects 表
CREATE TABLE IF NOT EXISTS Projects (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    github_id VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    description TEXT,
    url VARCHAR(255) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    language VARCHAR(50),
    stars_count INT NOT NULL DEFAULT 0,
    forks_count INT NOT NULL DEFAULT 0,
    watchers_count INT NOT NULL DEFAULT 0,
    open_issues_count INT NOT NULL DEFAULT 0,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    fetched_at DATETIME NOT NULL,
    trending_rank INT,
    is_favorite BOOLEAN NOT NULL DEFAULT FALSE,
    notes TEXT,
    UNIQUE KEY (github_id),
    INDEX (trending_rank),
    INDEX (language),
    INDEX (stars_count)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 ProjectTags 表
CREATE TABLE IF NOT EXISTS ProjectTags (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    count INT NOT NULL DEFAULT 0,
    UNIQUE KEY (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 ProjectTagMapping 表
CREATE TABLE IF NOT EXISTS ProjectTagMapping (
    project_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (project_id, tag_id),
    FOREIGN KEY (project_id) REFERENCES Projects(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES ProjectTags(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 Blogs 表
CREATE TABLE IF NOT EXISTS Blogs (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    cover_image VARCHAR(255),
    summary TEXT,
    category VARCHAR(50) NOT NULL,
    published BOOLEAN NOT NULL DEFAULT FALSE,
    published_at DATETIME,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    views_count INT NOT NULL DEFAULT 0,
    featured BOOLEAN NOT NULL DEFAULT FALSE,
    INDEX (category),
    INDEX (published_at),
    INDEX (featured)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 BlogTags 表
CREATE TABLE IF NOT EXISTS BlogTags (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    count INT NOT NULL DEFAULT 0,
    UNIQUE KEY (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 BlogTagMapping 表
CREATE TABLE IF NOT EXISTS BlogTagMapping (
    blog_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (blog_id, tag_id),
    FOREIGN KEY (blog_id) REFERENCES Blogs(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES BlogTags(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 ChatMessages 表
CREATE TABLE IF NOT EXISTS ChatMessages (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(50) NOT NULL,
    role VARCHAR(10) NOT NULL,
    content TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    related_project_id INT,
    FOREIGN KEY (related_project_id) REFERENCES Projects(id) ON DELETE SET NULL,
    INDEX (session_id),
    INDEX (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 Visitors 表
CREATE TABLE IF NOT EXISTS Visitors (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ip_address VARCHAR(45) NOT NULL,
    user_agent VARCHAR(255),
    visit_time DATETIME NOT NULL,
    page_url VARCHAR(255) NOT NULL,
    referer VARCHAR(255),
    country VARCHAR(50),
    city VARCHAR(50),
    INDEX (visit_time),
    INDEX (ip_address),
    INDEX (page_url)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建 SystemSettings 表
CREATE TABLE IF NOT EXISTS SystemSettings (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(50) NOT NULL,
    setting_value TEXT NOT NULL,
    description VARCHAR(255),
    updated_at DATETIME NOT NULL,
    UNIQUE KEY (setting_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建邮件订阅表
CREATE TABLE IF NOT EXISTS EmailSubscribers (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    name VARCHAR(50),
    subscribed_at DATETIME NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    confirmation_token VARCHAR(100),
    confirmed BOOLEAN NOT NULL DEFAULT FALSE,
    last_sent_at DATETIME,
    unsubscribe_token VARCHAR(100),
    UNIQUE KEY (email),
    INDEX (email),
    INDEX (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 初始化博主账户信息（固定ID为1）
INSERT INTO BlogOwner (id, username, password, email) 
VALUES (1, 'admin', '$2a$12$12345678901234567890abcdefabcde', 'your-email@example.com');

-- 添加一些常用系统设置
INSERT INTO SystemSettings (setting_key, setting_value, description, updated_at) VALUES
('site_title', '我的个人博客', '网站标题', NOW()),
('site_description', '分享技术和个人成长', '网站描述', NOW()),
('github_sync_interval', '86400', 'GitHub项目同步间隔（秒）', NOW()),
('posts_per_page', '10', '每页显示的博客文章数', NOW()),
('enable_visitor_tracking', 'true', '是否启用访客统计', NOW());

-- 提交事务
COMMIT; 