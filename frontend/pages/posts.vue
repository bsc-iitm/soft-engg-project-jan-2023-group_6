<template>
  <v-row justify="center" align="center">
    <v-card outlined style="width: 100%; padding: 20px">
      <div style="display: flex; gap: 40px">
        <span>Ticket #{{ ticket.id }}</span>
        <span style="margin-left: 40px"
          >Tags: {{ ticket.tags.join(', ') }}</span
        >
      </div>
      <v-card
        outlined
        style="
          width: 100%;
          padding: 4px;
          margin: 20px 0 30px 0;
          min-height: 130px;
          max-height: 130px;
          overflow: hidden;
        "
      >
        <v-card-title>{{ ticket.title }}</v-card-title>
        <v-card-subtitle>{{ ticket.content }}</v-card-subtitle>
      </v-card>

      <div
        style="
          display: flex;
          gap: 40px;
          align-items: center;
          justify-content: space-between;
        "
      >
        <span
          >Status:
          <span
            :style="{
              color: ticket.status == 'Open' ? 'red' : 'green',
              fontWeight: 700,
            }"
          >
            {{ ticket.status }}
          </span></span
        >
        <v-btn color="blue" style="color: white">View Details</v-btn>
      </div>
    </v-card>
  </v-row>
</template>

<script>
export default {
  name: 'PostsPage',
  middleware: 'authenticated',
  data() {
    return {
      ticket: {
        id: 234,
        tags: ['Course', 'Misc'],
        title: 'New course',
        content:
          'ADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJL ADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJLADKJ KJFLKJS KLJFLSDKJF LKSJFL KSJFLKJ SLKFJLKSD JFKLSDJFLKSDFJL',
        status: 'Resolved',
      },
    }
  },
}
</script>
