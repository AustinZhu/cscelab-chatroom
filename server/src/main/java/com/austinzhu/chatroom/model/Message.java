package com.austinzhu.chatroom.model;

import lombok.Data;
import lombok.Getter;
import lombok.NonNull;
import lombok.Setter;

import java.util.Date;


public record Message(

        @NonNull
        String channel,

        @NonNull
        String text,

        @NonNull
        Date createdAt,

        @NonNull
        String username
) {
}