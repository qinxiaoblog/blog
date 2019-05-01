CREATE TABLE `users` (
  `id`        SERIAL       NOT NULL,
  `nickname`  VARCHAR(64)  NOT NULL
  COMMENT '用户名',
  `email`     VARCHAR(128) NOT NULL
  COMMENT '用户注册邮箱',
  `description` VARCHAR(255) NOT NULL DEFAULT ''
  COMMENT '用户描述',
  `about_me`    TEXT NOT NULL
  COMMENT '个人详细介绍',
  `remark`    VARCHAR(255) NOT NULL DEFAULT ''
  COMMENT '备注',
  `is_drop`   TINYINT(4)   NOT NULL DEFAULT 0
  COMMENT '是否删除',
  `create_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
  ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE (`email`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  COMMENT = '用户表';


CREATE TABLE `local_auth` (
  `id`        SERIAL       NOT NULL,
  `user_id`   BIGINT       NOT NULL
  COMMENT '用户id',
  `password`  VARCHAR(128) NOT NULL
  COMMENT '用户密码',
  `remark`    VARCHAR(255) NOT NULL DEFAULT ''
  COMMENT '备注',
  `is_drop`   TINYINT(4)   NOT NULL DEFAULT 0
  COMMENT '是否删除',
  `create_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
  ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE (`user_id`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4
  COLLATE = utf8mb4_unicode_ci
  COMMENT = '本地验证表';

CREATE TABLE `blogs` (
  `id` SERIAL NOT NULL,
  `user_id` BIGINT NOT NULL COMMENT '博客拥有者id',
  `name` VARCHAR(64) NOT NULL COMMENT '博客名',
  `picture` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '头像',
  `description` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '博客描述',
  `remark` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '备注',
  `is_drop` TINYINT(4) NOT NULL DEFAULT 0 COMMENT '是否删除',
  `create_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
  )
  ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='博客表';
CREATE TABLE `categories` (
  `id` SERIAL NOT NULL,
  `user_id` BIGINT NOT NULL COMMENT '目录拥有用户id',
  `blog_id` BIGINT NOT NULL COMMENT '所在博客id',
  `name` VARCHAR(64) NOT NULL COMMENT '类别名',
  `description` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '类别描述',
  `position` INT NOT NULL DEFAULT 999 COMMENT '数字越大越靠后',
  `remark` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '备注',
  `is_drop` TINYINT(4) NOT NULL DEFAULT 0 COMMENT '是否删除',
  `create_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  unique idx_user_id_category (`user_id`, `name`),
  PRIMARY KEY (`id`)
  )ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='类别表';
CREATE TABLE `tags` (
  `id` SERIAL NOT NULL,
  `user_id` BIGINT NOT NULL COMMENT '标签拥有者id',
  `name` VARCHAR(64) NOT NULL COMMENT '标签名',
  `description` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '标签描述',
  `remark` VARCHAR(255) NOT NULL DEFAULT '' COMMENT '备注',
  `is_drop` TINYINT(4) NOT NULL DEFAULT 0 COMMENT '是否删除',
  `create_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  unique idx_user_id_tag (`user_id`, `name`),
  PRIMARY KEY (`id`)
  )ENGINE=InnoDB
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_unicode_ci
  COMMENT='标签表';