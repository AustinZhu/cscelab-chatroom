package com.austinzhu.chatroom.handler;

import com.austinzhu.chatroom.model.Message;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.socket.WebSocketHandler;
import org.springframework.web.reactive.socket.WebSocketMessage;
import org.springframework.web.reactive.socket.WebSocketSession;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Sinks;
import reactor.util.annotation.NonNull;

import java.util.Date;

@RequiredArgsConstructor
@Component
public class MessageHandler implements WebSocketHandler {

    private final Sinks.Many<Message> sink = Sinks.many().replay().limit(10);

    private final Flux<Message> output = sink.asFlux();

    @Override
    public Mono<Void> handle(@NonNull WebSocketSession session) {
        session.receive()
                .map(WebSocketMessage::getPayloadAsText)
                .map(s -> new Message("ch", s, new Date(), "user"))
                .doOnNext(System.out::println)
                .subscribe(
                        (s -> sink.emitNext(s, Sinks.EmitFailureHandler.FAIL_FAST)),
                        (e -> sink.emitError(e, Sinks.EmitFailureHandler.FAIL_FAST))
                );
        return session.send(output.map(
                o -> session.textMessage(o.text())
        ));
    }
}
