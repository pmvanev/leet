
template <typename item_t> class RingBuffer {
public:
  RingBuffer(size_t size)
      : m_size(size), m_buffer(std::make_unique<item_t[]>(size)), m_head(0),
        m_tail(0), m_items(0) {}

  bool empty() const { return !m_items; }

  bool full() const { return m_items == m_size; }

  bool enqueue(item_t item) {
    if (full) {
      return false;
    }
    m_buffer[m_tail++] = item;
    m_tail %= m_size;
    m_items++;
    return true;
  }

  std::optional<item_t> dequeue() {
    if (empty()) {
      return std::nullopt;
    }
    item_t dequeuedItem = m_buffer[m_head++];
    m_head %= m_size;
    m_items--;
    return dequeuedItem;
  }

private:
  const size_t m_size;
  std::unique_ptr<item_t[]> m_buffer;
  unsigned m_head{0}; // TODO: std::atomic for lock free queue?
  unsigned m_tail{0};
  unsigned m_items{0};
};

// NOTE: for pointer storate, simply use
// RingBuffer<std::shared_ptr<T>>(n_pointers);