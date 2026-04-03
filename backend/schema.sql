-- 论文选题系统数据库初始化脚本
-- Database: thesis_selection

CREATE DATABASE IF NOT EXISTS thesis_selection 
    DEFAULT CHARACTER SET utf8mb4 
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE thesis_selection;

-- 用户表
CREATE TABLE IF NOT EXISTS `user` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `password` VARCHAR(128) NOT NULL,
    `last_login` DATETIME(6) NULL,
    `is_superuser` TINYINT(1) NOT NULL DEFAULT 0,
    `username` VARCHAR(150) NOT NULL UNIQUE,
    `first_name` VARCHAR(150) NOT NULL DEFAULT '',
    `last_name` VARCHAR(150) NOT NULL DEFAULT '',
    `email` VARCHAR(254) NOT NULL DEFAULT '',
    `is_staff` TINYINT(1) NOT NULL DEFAULT 0,
    `is_active` TINYINT(1) NOT NULL DEFAULT 1,
    `date_joined` DATETIME(6) NOT NULL,
    `real_name` VARCHAR(50) NOT NULL,
    `role` INT NOT NULL DEFAULT 1 COMMENT '1:学生 2:教师 3:管理员',
    `student_id` VARCHAR(20) NULL COMMENT '学号',
    `teacher_id` VARCHAR(20) NULL COMMENT '工号',
    `phone` VARCHAR(11) NULL,
    `created_at` DATETIME(6) NOT NULL,
    `updated_at` DATETIME(6) NOT NULL,
    INDEX `idx_user_role` (`role`),
    INDEX `idx_user_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 论文题目表
CREATE TABLE IF NOT EXISTS `topic` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(200) NOT NULL,
    `description` TEXT NOT NULL,
    `requirements` TEXT,
    `max_students` INT UNSIGNED NOT NULL DEFAULT 1,
    `current_count` INT UNSIGNED NOT NULL DEFAULT 0,
    `teacher_id` BIGINT NOT NULL,
    `status` INT NOT NULL DEFAULT 1 COMMENT '1:开放 2:已满 3:关闭',
    `created_at` DATETIME(6) NOT NULL,
    `updated_at` DATETIME(6) NOT NULL,
    INDEX `idx_topic_teacher` (`teacher_id`),
    INDEX `idx_topic_status` (`status`),
    CONSTRAINT `fk_topic_teacher` FOREIGN KEY (`teacher_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 选题记录表
CREATE TABLE IF NOT EXISTS `selection` (
    `id` BIGINT AUTO_INCREMENT PRIMARY KEY,
    `student_id` BIGINT NOT NULL,
    `topic_id` BIGINT NOT NULL,
    `status` INT NOT NULL DEFAULT 1 COMMENT '1:待审批 2:已通过 3:已拒绝',
    `student_reason` TEXT,
    `teacher_comment` TEXT,
    `created_at` DATETIME(6) NOT NULL,
    `updated_at` DATETIME(6) NOT NULL,
    UNIQUE KEY `uk_student_topic` (`student_id`, `topic_id`),
    INDEX `idx_selection_student` (`student_id`),
    INDEX `idx_selection_topic` (`topic_id`),
    INDEX `idx_selection_status` (`status`),
    CONSTRAINT `fk_selection_student` FOREIGN KEY (`student_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_selection_topic` FOREIGN KEY (`topic_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
